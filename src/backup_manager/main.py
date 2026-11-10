import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    typelib_path = os.path.join(base_path, "gi_typelibs")
    os.environ["GI_TYPELIB_PATH"] = typelib_path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

from backup_manager.window import BackupWindow


class BackupApp(Gtk.Application):
    def __init__(self):
        # Initializes the BackupApp with a unique application ID and sets up the quit action
        super().__init__(
            application_id="com.example.LinuxBackup",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.window = None

    def on_quit_action(self, *_args):
        # When triggered, checks if the main window exists; if not, quits the application; otherwise, prompts the user for confirmation before quitting
        if self.window is None:
            self.quit()
            return
        self.window.confirm_quit()

    def do_activate(self):
        # Activates the application, creating and presenting the main window if it doesn't already exist
        if self.window is None:
            self.window = BackupWindow(self)
        self.window.present()