import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk, GLib


APP_DIR = Path.home() / ".config" / "linux-backup-manager"
PROCESSES_FILE = APP_DIR / "backup_processes.json"
PREFERENCES_FILE = APP_DIR / "preferences.json"
LOGGER = logging.getLogger(__name__)



class ProcessListMixin:
    def load_preferences(self):
        # Loads preferences from a JSON file
        try:
            with PREFERENCES_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            return
        except (OSError, json.JSONDecodeError):
            LOGGER.exception("Could not load application preferences")
            return

        if not isinstance(data, dict):
            LOGGER.warning("Ignoring invalid application preferences")
            return
        if data.get("language") in ("es", "en", "gl", "pt-PT"):
            self.language = data["language"]
        if isinstance(data.get("dark_theme"), bool):
            self.dark_theme = data["dark_theme"]

    def save_preferences(self):
        # Saves preferences to a JSON file
        APP_DIR.mkdir(parents=True, exist_ok=True)
        temporary = PREFERENCES_FILE.with_suffix(".tmp")
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(
                {"language": self.language, "dark_theme": self.dark_theme},
                handle,
                indent=2,
            )
        temporary.replace(PREFERENCES_FILE)

    def load_processes(self):
        # Loads backup processes from a JSON file.
        try:
            with PROCESSES_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            self.processes = []
            return

        self.processes = data if isinstance(data, list) else []
        schedules_changed = False
        for process in self.processes:
            if not isinstance(process, dict):
                continue
            process.setdefault("paused", False)
            if not isinstance(process.get("history"), list):
                history = []
                last_run = process.get("last_run")
                if last_run:
                    history.append(
                        {
                            "timestamp": last_run,
                            "success": True,
                            "target": "",
                        }
                    )
                process["history"] = history
                schedules_changed = True
            if not isinstance(process.get("sources"), list) or (
                not process.get("sources") and process.get("source")
            ):
                legacy_source = process.get("source")
                process["sources"] = [legacy_source] if legacy_source else []
                schedules_changed = True
            try:
                datetime.fromisoformat(process.get("next_run", ""))
                continue
            except (TypeError, ValueError):
                pass

            try:
                interval = max(1, int(process.get("interval_hours", 24)))
            except (TypeError, ValueError):
                LOGGER.warning(
                    "Invalid backup interval for process %r; using 24 hours",
                    process.get("id"),
                )
                interval = 24
            last_run = process.get("last_run")
            try:
                next_run = (
                    datetime.fromisoformat(last_run) + timedelta(hours=interval)
                    if last_run
                    else None
                )
            except (TypeError, ValueError):
                LOGGER.warning(
                    "Invalid last-run time for backup process %r; "
                    "scheduling its next run from the configured start time",
                    process.get("id"),
                )
                next_run = None
            if next_run is None:
                start_time = process.get("start_time", "09:00")
                try:
                    datetime.strptime(start_time, "%H:%M")
                except (TypeError, ValueError):
                    LOGGER.warning(
                        "Invalid start time for backup process %r; "
                        "using 09:00",
                        process.get("id"),
                    )
                    start_time = "09:00"
                next_run = self.first_scheduled_run(
                    start_time
                )
            process["next_run"] = next_run.isoformat(timespec="seconds")
            schedules_changed = True
        if schedules_changed:
            try:
                self.save_processes()
            except OSError:
                LOGGER.exception("Could not save migrated backup schedules")

    def save_processes(self):
        # Saves backup processes to a JSON file.
        APP_DIR.mkdir(parents=True, exist_ok=True)
        temporary = PROCESSES_FILE.with_suffix(".tmp")
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(self.processes, handle, indent=2)
        temporary.replace(PROCESSES_FILE)

    def build_process_list_page(self):
        # Builds the UI page that displays the list of backups.
        display = Gdk.Display.get_default()
        if display is not None:
            provider = Gtk.CssProvider()
            provider.load_from_data(
                b".backup-process-card { border-radius: 12px; } "
                b".backup-process-card.paused { "
                b"background-color: rgba(0, 0, 0, 0.18); "
                b"}"
            )
            Gtk.StyleContext.add_provider_for_display(
                display,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        page.set_margin_top(24)
        page.set_margin_bottom(24)
        page.set_margin_start(28)
        page.set_margin_end(28)

        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        heading = Gtk.Label(label=self.tr("processes"))
        heading.add_css_class("title-1")
        heading.set_xalign(0)
        heading.set_hexpand(True)
        self.processes_heading = heading
        top.append(heading)

        add_button = Gtk.Button(label=self.tr("new_backup"))
        add_button.add_css_class("suggested-action")
        add_button.connect("clicked", lambda _b: self.new_backup())
        self.new_backup_button = add_button
        top.append(add_button)
        page.append(top)

        scroller = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.process_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=12
        )
        scroller.set_child(self.process_list)
        page.append(scroller)
        return page

    def refresh_process_list(self):
        # Refreshes the list of backup processes displayed in the UI.
        self.process_widgets = {}
        child = self.process_list.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.process_list.remove(child)
            child = next_child

        if not self.processes:
            empty = Gtk.Label(
                label=self.tr("empty_process_list")
            )
            empty.set_justify(Gtk.Justification.CENTER)
            empty.set_margin_top(50)
            empty.add_css_class("dim-label")
            self.process_list.append(empty)
            return

        for index, process in enumerate(self.processes):
            card = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=10
            )
            card.set_margin_top(4)
            card.set_margin_bottom(4)
            card.set_margin_start(4)
            card.set_margin_end(4)
            card.add_css_class("card")
            card.add_css_class("backup-process-card")
            if process.get("paused", False):
                card.add_css_class("paused")

            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=12
            )

            details = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=5
            )
            details.set_hexpand(True)

            # Nombre del proceso
            name_row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=8,
            )
            name = Gtk.Button(
                label=process.get("name", self.tr("backup_default_name"))
            )
            name.set_has_frame(False)
            name.add_css_class("flat")
            name.add_css_class("heading")
            name.set_halign(Gtk.Align.START)
            name.set_hexpand(True)
            name.set_tooltip_text(self.tr("history_tooltip"))
            name.connect(
                "clicked",
                lambda _button, identifier=process["id"]:
                    self.show_backup_history(identifier),
            )
            name_row.append(name)
            paused = bool(process.get("paused", False))
            paused_status = Gtk.Label()
            paused_status.set_markup(f"<b>{self.tr('paused_status')}</b>")
            paused_status.set_visible(paused)
            name_row.append(paused_status)
            details.append(name_row)

            # Origen
            sources = process.get("sources") or [process.get("source", "")]
            source = Gtk.Label(
                label=self.tr("source_label")
                + "\n"
                + "\n".join(path for path in sources if path)
            )
            source.set_xalign(0)
            source.set_wrap(True)
            source.set_selectable(True)
            details.append(source)

            # Destino
            destination = Gtk.Label(
                label=self.tr("destination_label")
                + f" {process.get('destination', '')}"
            )
            destination.set_xalign(0)
            destination.set_wrap(True)
            destination.set_selectable(True)
            details.append(destination)

            # Intervalo en horas y equivalencia
            interval = max(1, int(process.get("interval_hours", 24)))

            if interval % 168 == 0:
                weeks = interval // 168
                equivalent = self.tr("week_count").format(count=weeks)
            elif interval % 24 == 0:
                days = interval // 24
                equivalent = self.tr("day_count").format(count=days)
            else:
                days_float = interval / 24
                equivalent = self.tr("fractional_days").format(
                    days=days_float
                )

            schedule = Gtk.Label(
                label=(
                    self.tr("frequency_label")
                    + f" {interval} "
                    + self.tr("hours")
                    + f" ({equivalent})"
                )
            )
            schedule.set_xalign(0)
            schedule.add_css_class("dim-label")
            details.append(schedule)

            # Hora de comienzo
            start_time = process.get("start_time", "09:00")
            start_label = Gtk.Label(
                label=self.tr("start_time_label")
                + f" {start_time}"
            )
            start_label.set_xalign(0)
            start_label.add_css_class("dim-label")
            details.append(start_label)

            # Exclusiones
            excluded = process.get("exclude", [])
            if excluded:
                excluded_label = Gtk.Label(
                    label=self.tr("exclusion_count").format(
                        count=len(excluded)
                    )
                )
                excluded_label.set_xalign(0)
                excluded_label.add_css_class("dim-label")
                details.append(excluded_label)

            row.append(details)

            # Botones de acciones
            actions = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=6
            )

            edit = Gtk.Button(
                label=self.tr("edit_action")
            )
            edit.connect("clicked", self.edit_process, process["id"])
            actions.append(edit)

            run = Gtk.Button(label=self.tr("run_now"))
            run.connect("clicked", self.run_process, process["id"])
            run.set_sensitive(not self.busy)
            actions.append(run)

            pause = Gtk.Button(
                label=self.tr("resume")
                if paused
                else self.tr("pause")
            )
            pause.connect("clicked", self.toggle_process_paused, process["id"])
            actions.append(pause)

            remove = Gtk.Button(
                label=self.tr("remove_action")
            )
            remove.add_css_class("destructive-action")
            remove.connect("clicked", self.remove_process, process["id"])
            actions.append(remove)

            row.append(actions)
            card.append(row)
            self.process_list.append(card)
            self.process_widgets[process["id"]] = (
                card,
                run,
                pause,
                paused_status,
            )
            if index < len(self.processes) - 1:
                self.process_list.append(
                    Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                )

    @staticmethod
    def format_interval(hours):
        # Formats an interval in hours into a string. It can also be converted to days if needed.
        hours = int(hours)
        if hours < 24:
            return f"{hours} hour(s)"
        if hours % 24 == 0:
            days = hours // 24
            return f"{days} day(s)"
        return f"{hours} hour(s)"

    def show_processes(self, *_args):
        # Displays the list of backup processes in the UI.
        self.refresh_process_list()
        self.stack.set_visible_child_name("processes")
        self.header_title.set_text(self.tr("app_title"))

    def show_backup_history(self, process_id):
        # Displays the backup history for a specific process (in a new window).
        process = self.find_process(process_id)
        if not process:
            return

        history_window = Gtk.Window(
            transient_for=self,
            modal=True,
            title=self.tr("history_title").format(
                name=process.get("name", self.tr("backup_default_name"))
            ),
        )
        history_window.set_default_size(680, 480)
        self.history_window = history_window

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        content.set_margin_top(18)
        content.set_margin_bottom(18)
        content.set_margin_start(18)
        content.set_margin_end(18)

        history_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        history = process.get("history", [])
        if not isinstance(history, list):
            history = []
        if not history:
            empty = Gtk.Label(label=self.tr("history_empty"))
            empty.set_xalign(0)
            empty.add_css_class("dim-label")
            history_list.append(empty)
        else:
            for entry in reversed(history):
                if not isinstance(entry, dict):
                    continue
                timestamp = entry.get("timestamp", "")
                try:
                    date = datetime.fromisoformat(timestamp).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                except (TypeError, ValueError):
                    date = str(timestamp)

                success = entry.get("success") is True
                status = self.tr(
                    "history_success" if success else "history_failed"
                )
                run_type = self.tr(
                    "history_unknown_type"
                    if "scheduled" not in entry
                    else (
                        "history_scheduled"
                        if entry["scheduled"]
                        else "history_manual"
                    )
                )
                summary = Gtk.Label(
                    label=self.tr("history_entry").format(
                        date=date,
                        status=status,
                        run_type=run_type,
                    )
                )
                summary.set_xalign(0)
                summary.add_css_class("heading")
                history_list.append(summary)

                if success:
                    target = entry.get("target")
                    location = Gtk.Label(
                        label=(
                            self.tr("history_saved_to").format(path=target)
                            if target
                            else self.tr("history_location_unknown")
                        )
                    )
                    location.set_xalign(0)
                    location.set_selectable(True)
                    location.set_wrap(True)
                    history_list.append(location)
                else:
                    error_key = entry.get("error_key", "backup_failed")
                    if error_key not in self.translations["en"]:
                        error_key = "backup_failed"
                    error_detail = entry.get("error_detail", "")
                    error = self.tr(error_key)
                    if error_detail:
                        error = error.format(error=error_detail)
                    error_label = Gtk.Label(
                        label=self.tr("history_error").format(error=error)
                    )
                    error_label.set_xalign(0)
                    error_label.set_wrap(True)
                    history_list.append(error_label)

                history_list.append(
                    Gtk.Separator(
                        orientation=Gtk.Orientation.HORIZONTAL
                    )
                )

        scroller = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        scroller.set_child(history_list)
        content.append(scroller)

        close_button = Gtk.Button(label=self.tr("close"))
        close_button.set_halign(Gtk.Align.END)
        close_button.connect(
            "clicked",
            lambda _button: history_window.close(),
        )
        content.append(close_button)
        history_window.set_child(content)
        history_window.present()

    def remove_process(self, _button, process_id):
        # Prompts confirmation to remove a backup process and removes it if confirmed.
        process = self.find_process(process_id)
        if not process:
            return
        dialog = Gtk.AlertDialog(
            message=self.tr("remove_process_confirm").format(
                name=process.get("name", self.tr("backup_default_name"))
            ),
            detail=self.tr("remove_process_detail"),
            buttons=[self.tr("cancel"), self.tr("remove_action")],
            cancel_button=0,
            default_button=1,
        )
        dialog.choose(self, None, self.on_remove_response, process_id)

    def toggle_process_paused(self, button, process_id):
        # Toggles the paused state of a backup process and updates the UI accordingly.
        process = self.find_process(process_id)
        if not process:
            return
        previous_paused = bool(process.get("paused", False))
        process["paused"] = not previous_paused
        try:
            self.save_processes()
        except OSError as error:
            process["paused"] = previous_paused
            LOGGER.exception("Could not save pause state for backup process")
            self.show_error(self.tr("save_error").format(error=error))
            return
        widgets = self.process_widgets.get(process_id)
        if widgets:
            card, _run_button, pause_button, paused_status = widgets
            paused = process["paused"]
            pause_button.set_label(
                self.tr("resume") if paused else self.tr("pause")
            )
            paused_status.set_markup(
                f"<b>{self.tr('paused_status')}</b>"
            )
            paused_status.set_visible(paused)
            if paused:
                card.add_css_class("paused")
            else:
                card.remove_css_class("paused")

    def set_backup_running_state(self, busy):
        # Sets the running state of the backup processes, enabling or disabling the "Run Now" buttons accordingly.
        self.busy = busy
        for _card, run_button, _pause_button, _status in (
            self.process_widgets.values()
        ):
            run_button.set_sensitive(not busy)

    def on_remove_response(self, dialog, result, process_id):
        # Handles the user's decision to remove a backup process.
        try:
            response = dialog.choose_finish(result)
        except GLib.Error:
            return
        if response == 1:
            self.processes = [
                p for p in self.processes if p.get("id") != process_id
            ]
            self.save_processes()
            self.refresh_process_list()

    def find_process(self, process_id):
        # Finds a backup process using its ID.
        return next(
            (p for p in self.processes if p.get("id") == process_id), None
        )
