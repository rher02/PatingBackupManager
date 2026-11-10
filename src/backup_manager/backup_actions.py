import fnmatch
import logging
import os
import shutil
import threading
from datetime import datetime, timedelta

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib


LOGGER = logging.getLogger(__name__)


class BackupActionsMixin:
    def run_process(self, _button, process_id):
        # Initiates the backup process for an specific process ID (if it's not running)
        process = self.find_process(process_id)
        if not process or self.busy:
            return
        self.run_backup(process)

    def run_backup(self, process, scheduled=False):
        # Runs the backup process with error handling
        configured_sources = process.get("sources")
        if not isinstance(configured_sources, list):
            legacy_source = process.get("source")
            configured_sources = [legacy_source] if legacy_source else []
        configured_destination = process.get("destination")
        if (
            not configured_sources
            or any(
                not isinstance(source, str) or not source.strip()
                for source in configured_sources
            )
            or not isinstance(configured_destination, str)
            or not configured_destination.strip()
        ):
            self.handle_backup_error(
                process,
                "backup_source_unconfigured",
                scheduled,
            )
            return
        sources = list(
            dict.fromkeys(os.path.realpath(path) for path in configured_sources)
        )
        destination = os.path.realpath(configured_destination)
        if not os.path.isdir(destination) or any(
            not os.path.isdir(source) for source in sources
        ):
            self.handle_backup_error(
                process,
                "backup_source_missing",
                scheduled,
            )
            return
        for index, source in enumerate(sources):
            # Check for overlapping paths between sources and destination
            try:
                common = os.path.commonpath([source, destination])
            except ValueError:
                common = None
            if common in (source, destination):
                self.handle_backup_error(
                    process,
                    "backup_paths_overlap",
                    scheduled,
                )
                return
            for other_source in sources[index + 1:]:
                try:
                    common = os.path.commonpath([source, other_source])
                except ValueError:
                    common = None
                if common in (source, other_source):
                    self.handle_backup_error(
                        process,
                        "backup_sources_overlap",
                        scheduled,
                    )
                    return

        # Creates a UNIQUE target directory for the backup
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = os.path.basename(sources[0].rstrip(os.sep)) or "backup"
        target_name = f"{backup_name}_{timestamp}"
        target = os.path.join(destination, target_name)
        suffix = 1
        while os.path.exists(target):
            target = os.path.join(destination, f"{target_name}_{suffix}")
            suffix += 1
        exclusions = set(process.get("exclude", []))

        self.set_backup_running_state(True)
        self.header_title.set_text(self.tr("app_title"))
        scheduled_for = process.get("next_run") if scheduled else None

        def make_ignore(source):
            def ignore(directory, names):
                ignored = []
                for name in names:
                    full = os.path.join(directory, name)
                    relative = os.path.relpath(full, source)
                    for pattern in exclusions:
                        if relative == pattern or relative.startswith(
                            pattern.rstrip(os.sep) + os.sep
                        ) or fnmatch.fnmatch(name, pattern):
                            ignored.append(name)
                            break
                return ignored

            return ignore

        def worker():
            # Performs the backup operation in a separate thread to avoid blocking the UI
            try:
                if len(sources) == 1:
                    shutil.copytree(
                        sources[0],
                        target,
                        copy_function=shutil.copy2,
                        ignore=make_ignore(sources[0]),
                    )
                else:
                    os.makedirs(target)
                    for index, source in enumerate(sources, start=1):
                        source_name = os.path.basename(source.rstrip(os.sep))
                        source_target = os.path.join(
                            target, f"{index:02d}_{source_name or 'source'}"
                        )
                        shutil.copytree(
                            source,
                            source_target,
                            copy_function=shutil.copy2,
                            ignore=make_ignore(source),
                        )
                GLib.idle_add(
                    self.backup_done,
                    process["id"],
                    target,
                    None,
                    scheduled,
                    scheduled_for,
                )
            except Exception as error:
                # Error logging and handling (if it fails)
                LOGGER.exception(
                    "Backup failed for process %r",
                    process.get("id"),
                )
                GLib.idle_add(
                    self.backup_done,
                    process["id"],
                    target,
                    str(error),
                    scheduled,
                    scheduled_for,
                )

        threading.Thread(target=worker, daemon=True).start()

    def backup_done(
        self,
        process_id,
        target,
        error,
        scheduled=False,
        scheduled_for=None,
    ):
        # Updates the process history and schedule after the backup operation is completed, handling success or failure
        self.set_backup_running_state(False)
        process = self.find_process(process_id)
        if process:
            now = datetime.now()
            history_entry = {
                "timestamp": now.isoformat(timespec="seconds"),
                "success": not error,
                "target": target if not error else "",
                "scheduled": bool(scheduled),
            }
            if error:
                history_entry["error_key"] = "backup_failed"
                history_entry["error_detail"] = error
            history = process.get("history")
            if not isinstance(history, list):
                history = []
                process["history"] = history
            history.append(history_entry)
            if not error:
                process["last_run"] = now.isoformat(timespec="seconds")
            if scheduled and scheduled_for:
                due_time = self.parse_schedule_time(scheduled_for)
                if error:
                    next_run = now + timedelta(
                        hours=max(1, int(process.get("interval_hours", 24)))
                    )
                else:
                    next_run = self.next_scheduled_run(
                        due_time,
                        process.get("interval_hours", 24),
                        now,
                    )
                process["next_run"] = next_run.isoformat(timespec="seconds")
            elif not error:
                process["next_run"] = (
                    now
                    + timedelta(
                        hours=max(1, int(process.get("interval_hours", 24)))
                    )
                ).isoformat(timespec="seconds")
            try:
                self.save_processes()
            except OSError as save_error:
                LOGGER.exception("Could not save backup history and schedule")
                if self.is_visible():
                    self.show_error(
                        self.tr("save_schedule_error").format(
                            error=save_error
                        )
                    )

        self.refresh_process_list()
        self.header_title.set_text(self.tr("app_title"))
        if error:
            if self.is_visible():
                self.show_error(
                    self.tr("backup_failed").format(error=error)
                )
            else:
                LOGGER.error("Backup failed: %s", error)
        else:
            message = (
                self.tr("backup_completed")
                + "\n"
                + self.tr("backup_completed_location").format(path=target)
            )
            if self.is_visible():
                self.show_info(message)
            else:
                LOGGER.info(message)
        return GLib.SOURCE_REMOVE

    def handle_backup_error(self, process, error_key, scheduled):
        # Handles errors during the backup process, notifying the user
        now = datetime.now()
        history = process.get("history")
        if not isinstance(history, list):
            history = []
            process["history"] = history
        history.append(
            {
                "timestamp": now.isoformat(timespec="seconds"),
                "success": False,
                "target": "",
                "error_key": error_key,
                "error_detail": "",
                "scheduled": bool(scheduled),
            }
        )
        if scheduled:
            process["next_run"] = (
                now
                + timedelta(
                    hours=max(1, int(process.get("interval_hours", 24)))
                )
            ).isoformat(timespec="seconds")
        try:
            self.save_processes()
        except OSError as save_error:
            LOGGER.exception("Could not save failed backup history")
            if self.is_visible():
                self.show_error(
                    self.tr("save_schedule_error").format(
                        error=save_error
                    )
                )
        message = self.tr(error_key)
        if self.is_visible():
            self.show_error(message)
        else:
            LOGGER.error(message)

    def show_error(self, message):
        # Shows an error dialog with custom message
        dialog = Gtk.AlertDialog(message=message)
        dialog.show(self)

    def show_info(self, message):
        # Shows an informative dialog with custom message
        self.show_notification(message)
