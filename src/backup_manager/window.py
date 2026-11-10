from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gdk, Gtk, Gio, GLib
if __package__:
    from .backup_actions import BackupActionsMixin
    from .editor import BackupEditorMixin
    from .localization import LocalizationMixin, TRANSLATIONS
    from .processes import ProcessListMixin
    from .scheduler import ScheduledBackupsMixin
else:
    from backup_actions import BackupActionsMixin
    from editor import BackupEditorMixin
    from localization import LocalizationMixin, TRANSLATIONS
    from processes import ProcessListMixin
    from scheduler import ScheduledBackupsMixin

from .resources import get_asset_path

css_path = get_asset_path("header.css")

provider = Gtk.CssProvider()
provider.load_from_path(str(css_path))

class BackupWindow(
    Gtk.ApplicationWindow,
    LocalizationMixin,
    ProcessListMixin,
    BackupEditorMixin,
    ScheduledBackupsMixin,
    BackupActionsMixin,
):
    def get_dark_theme_preference(self):
        # Determines the user's preference for dark theme based on GTK settings.
        if self.settings.find_property("gtk-interface-color-scheme"):
            return (
                self.settings.get_property("gtk-interface-color-scheme")
                == Gtk.InterfaceColorScheme.DARK
            )
        if self.settings.find_property(
            "gtk-application-prefer-dark-theme"
        ):
            return bool(
                self.settings.get_property(
                    "gtk-application-prefer-dark-theme"
                )
            )
        return False

    def set_dark_theme_preference(self, dark_theme):
        # Sets the user's preference for dark theme in GTK settings.
        if self.settings.find_property("gtk-interface-color-scheme"):
            color_scheme = (
                Gtk.InterfaceColorScheme.DARK
                if dark_theme
                else Gtk.InterfaceColorScheme.LIGHT
            )
            self.settings.set_property(
                "gtk-interface-color-scheme", color_scheme
            )
        elif self.settings.find_property(
            "gtk-application-prefer-dark-theme"
        ):
            self.settings.set_property(
                "gtk-application-prefer-dark-theme", dark_theme
            )

    def __init__(self, app):
        # Initializes the BackupWindow, sets up the UI components, and loads user preferences and processes.
        super().__init__(
            application=app,
            title="Backup Manager",
            default_width=960,
            default_height=800,
        )
        self.processes = []
        self.editing_id = None
        self.sources = []
        self.destination = ""
        self.excluded_paths = []
        self.busy = False

        self.language = "en"
        self.dark_theme = None

        self.translations = TRANSLATIONS

        self.load_preferences()
        self.load_processes()
        self.set_title(self.tr("app_title"))

        self.stack = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
            transition_duration=180,
            vexpand=True,
        )
        self.stack.add_named(self.build_process_list_page(), "processes")
        self.stack.add_named(self.build_editor_page(), "editor")
        self.connect("close-request", self.on_close_request)

        self.toast_timeout_id = 0
        self.content_overlay = Gtk.Overlay()
        self.content_overlay.set_child(self.stack)
        self.toast_revealer = Gtk.Revealer()
        self.toast_revealer.set_transition_type(
            Gtk.RevealerTransitionType.SLIDE_UP
        )
        self.toast_revealer.set_halign(Gtk.Align.END)
        self.toast_revealer.set_valign(Gtk.Align.END)
        self.toast_revealer.set_margin_end(24)
        self.toast_revealer.set_margin_bottom(24)
        self.toast_revealer.set_can_target(False)
        self.toast_revealer.add_css_class("osd")
        toast_frame = Gtk.Frame()
        toast_frame.add_css_class("card")
        self.toast_label = Gtk.Label()
        self.toast_label.set_xalign(0)
        self.toast_label.set_wrap(True)
        self.toast_label.set_selectable(True)
        self.toast_label.set_margin_top(12)
        self.toast_label.set_margin_bottom(12)
        self.toast_label.set_margin_start(16)
        self.toast_label.set_margin_end(16)
        toast_frame.set_child(self.toast_label)
        self.toast_revealer.set_child(toast_frame)
        self.content_overlay.add_overlay(self.toast_revealer)
        self.content_overlay.set_measure_overlay(self.toast_revealer, False)

        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)
        header.add_css_class("patterned-header")

        display = Gdk.Display.get_default()
        if display is not None:
            self.header_css_provider = Gtk.CssProvider()
            self.header_css_provider.load_from_path(
                str(get_asset_path("header.css"))
            )
            Gtk.StyleContext.add_provider_for_display(
                display,
                self.header_css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

        self.settings = Gtk.Settings.get_default()
        if self.dark_theme is None:
            self.dark_theme = self.get_dark_theme_preference()
        self.set_dark_theme_preference(self.dark_theme)

        self.theme_button = Gtk.Button()
        self.theme_button.connect("clicked", self.toggle_theme)
        header.pack_start(self.theme_button)

        # Título centrado
        self.header_title = Gtk.Label(label=self.tr("app_title"))
        self.header_title.add_css_class("title")
        header.set_title_widget(self.header_title)

        self.set_titlebar(header)
        self.update_theme_button()

        menu_button = Gtk.MenuButton()
        self.quit_menu = Gio.Menu()
        self.quit_menu.append(self.tr("quit"), "app.quit")
        menu_button.set_menu_model(self.quit_menu)
        self.language_selector = Gtk.DropDown.new_from_strings(
            ["Español", "English", "Galego", "Português (Portugal)"]
        )
        language_codes = tuple(TRANSLATIONS)
        self.language_selector.set_selected(
            language_codes.index(self.language)
            if self.language in language_codes
            else 1
        )
        self.language_selector.connect(
            "notify::selected",
            self.on_language_changed
        )
        header.pack_start(self.language_selector)
        header.pack_start(menu_button)
        self.set_titlebar(header)

        for name, callback in (
            ("show-processes", self.show_processes),
            ("new-backup", self.new_backup),
        ):
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)

        self.set_child(self.content_overlay)
        self.show_processes()
        self.start_backup_scheduler()

    def confirm_quit(self):
        # Asks the user for confirmation beore quitting the app
        dialog = Gtk.AlertDialog(
            message=self.tr("quit_confirm_title"),
            detail=self.tr("quit_confirm_detail"),
            buttons=[self.tr("cancel"), self.tr("quit")],
            cancel_button=0,
            default_button=1,
        )
        dialog.choose(self, None, self.on_quit_confirmation, None)

    def on_quit_confirmation(self, dialog, result, _user_data):
        # Handles the user's response to the quit confirmation dialog.
        try:
            response = dialog.choose_finish(result)
        except GLib.Error:
            return
        if response == 1:
            self.get_application().quit()

    def show_notification(self, message):
        # Displays a temporary notification message to the user for 5 seconds.
        self.toast_label.set_text(message)
        self.toast_revealer.set_reveal_child(True)
        if self.toast_timeout_id:
            GLib.source_remove(self.toast_timeout_id)
        self.toast_timeout_id = GLib.timeout_add_seconds(
            5,
            self.hide_notification,
        )

    def hide_notification(self):
        # Hides the notification message and resets the timeout ID.
        self.toast_revealer.set_reveal_child(False)
        self.toast_timeout_id = 0
        return GLib.SOURCE_REMOVE

    def on_close_request(self, _window):
        # Handles the window close request by hiding the window instead of closing it, allowing for background operation.
        self.set_visible(False)
        return True
