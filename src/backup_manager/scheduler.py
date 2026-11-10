import logging
from datetime import datetime, timedelta

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib


LOGGER = logging.getLogger(__name__)
SCHEDULER_INTERVAL_SECONDS = 30


class ScheduledBackupsMixin:
    def start_backup_scheduler(self):
        # Starts the backup scheduler by setting up a periodic check for scheduled backups.
        GLib.timeout_add_seconds(
            SCHEDULER_INTERVAL_SECONDS,
            self.check_scheduled_backups,
        )
        self.check_scheduled_backups()

    @staticmethod
    def parse_schedule_time(value):
        # Parses a scheduled time string into a datetime object, adjusting for timezone too.
        scheduled = datetime.fromisoformat(value)
        if scheduled.tzinfo is not None:
            scheduled = scheduled.astimezone().replace(tzinfo=None)
        return scheduled

    @staticmethod
    def first_scheduled_run(start_time, now=None):
        # Calculates the first scheduled run time.
        # If the calculated scheduled time is in the past, it adjusts to the next day to prevent errors.
        now = now or datetime.now()
        scheduled_time = datetime.strptime(start_time, "%H:%M").time()
        scheduled = datetime.combine(now.date(), scheduled_time)
        if scheduled <= now:
            scheduled += timedelta(days=1)
        return scheduled

    @staticmethod
    def next_scheduled_run(previous_run, interval_hours, now=None):
        # Calculates the next scheduled run time based on the previous run and the specified interval in hours.
        now = now or datetime.now()
        interval = timedelta(hours=max(1, int(interval_hours)))
        elapsed = now - previous_run
        intervals_elapsed = max(0, elapsed // interval)
        return previous_run + interval * (intervals_elapsed + 1)

    def check_scheduled_backups(self):
        # Checks for scheduled backups that are due to run.
        if self.busy:
            return GLib.SOURCE_CONTINUE

        now = datetime.now()
        due_processes = []
        for process in self.processes:
            if process.get("paused", False):
                continue
            try:
                next_run = self.parse_schedule_time(process["next_run"])
            except (KeyError, TypeError, ValueError):
                LOGGER.exception(
                    "Invalid next-run time for backup process %r",
                    process.get("id"),
                )
                continue
            if next_run <= now:
                due_processes.append((next_run, process))

        if due_processes:
            _, process = min(due_processes, key=lambda item: item[0])
            self.run_backup(process, scheduled=True)
        return GLib.SOURCE_CONTINUE
