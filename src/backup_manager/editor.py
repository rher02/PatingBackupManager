import os
from datetime import datetime

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk



class BackupEditorMixin:
    def build_editor_page(self):
        # Main editor page layout
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_top(24)
        page.set_margin_bottom(24)
        page.set_margin_start(28)
        page.set_margin_end(28)

        # Editor heading
        heading = Gtk.Label(label=self.tr("new_backup"))
        heading.add_css_class("title-1")
        heading.set_xalign(0)
        self.editor_heading = heading
        page.append(heading)

        # Form inside a scrolled window
        scroller = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        form.set_margin_end(8)
        scroller.set_child(form)
        page.append(scroller)

        # Editor fields: name, source, destination, interval, start time and exclude
        self.editor_labels = {}
        self.editor_labels["name"] = self.field_label(self.tr("name"))
        form.append(self.editor_labels["name"])
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text(self.tr("name_placeholder"))
        form.append(self.name_entry)

        self.editor_labels["source"] = self.field_label(self.tr("source"))
        form.append(self.editor_labels["source"])
        source_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.source_list = Gtk.ListBox()
        self.source_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.source_list.set_hexpand(True)
        source_row.append(self.source_list)
        self.source_button = Gtk.Button(label=self.tr("add_source"))
        self.source_button.connect("clicked", self.choose_source)
        source_row.append(self.source_button)
        form.append(source_row)

        self.editor_labels["destination"] = self.field_label(
            self.tr("destination")
        )
        form.append(self.editor_labels["destination"])
        dest_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.dest_label = Gtk.Label(label=self.tr("no_destination"))
        self.dest_label.set_xalign(0)
        self.dest_label.set_wrap(True)
        self.dest_label.set_hexpand(True)
        dest_row.append(self.dest_label)
        self.destination_button = Gtk.Button(label=self.tr("choose_folder"))
        self.destination_button.connect("clicked", self.choose_destination)
        dest_row.append(self.destination_button)
        form.append(dest_row)

        self.editor_labels["interval"] = self.field_label(
            self.tr("interval")
        )
        form.append(self.editor_labels["interval"])
        interval_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.interval_spin = Gtk.SpinButton.new_with_range(1, 8760, 1)
        self.interval_spin.set_value(24)
        interval_row.append(self.interval_spin)
        self.interval_unit = 0
        self.interval_unit_dropdown = Gtk.DropDown.new_from_strings(
            [self.tr("hours"), self.tr("days")]
        )
        self.interval_unit_dropdown.set_selected(self.interval_unit)
        self.interval_unit_dropdown.connect(
            "notify::selected", self.on_interval_unit_changed
        )
        interval_row.append(self.interval_unit_dropdown)
        self.day_equivalence_label = Gtk.Label(
            label=self.tr("day_equivalence"), css_classes=["dim-label"]
        )
        interval_row.append(self.day_equivalence_label)
        form.append(interval_row)

        self.editor_labels["start_time"] = self.field_label(
            self.tr("start_time")
        )
        form.append(self.editor_labels["start_time"])
        self.start_time_entry = Gtk.Entry()
        self.start_time_entry.set_text("09:00")
        self.start_time_entry.set_placeholder_text(
            self.tr("start_time_placeholder")
        )
        self.start_time_entry.set_input_purpose(Gtk.InputPurpose.DIGITS)
        form.append(self.start_time_entry)
        self.start_time_description = Gtk.Label(
            label=self.tr("start_time_schedule_description")
        )
        self.start_time_description.set_xalign(0)
        self.start_time_description.set_wrap(True)
        self.start_time_description.add_css_class("dim-label")
        form.append(self.start_time_description)

        self.editor_labels["exclude"] = self.field_label(self.tr("exclude"))
        form.append(self.editor_labels["exclude"])
        self.exclude_description = Gtk.Label(
            label=self.tr("exclude_description")
        )
        self.exclude_description.set_xalign(0)
        self.exclude_description.set_wrap(True)
        self.exclude_description.add_css_class("dim-label")
        form.append(self.exclude_description)

        exclude_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.exclude_entry = Gtk.Entry()
        self.exclude_entry.set_placeholder_text(self.tr("exclude_placeholder"))
        self.exclude_entry.set_hexpand(True)
        exclude_row.append(self.exclude_entry)
        #self.add_exclusion_button = Gtk.Button(label=self.tr("add_path"))
        #self.add_exclusion_button.connect("clicked", self.add_exclusion)
        #exclude_row.append(self.add_exclusion_button)
        self.choose_exclusion_file_button = Gtk.Button(
            label=self.tr("choose_exclusion_file")
        )
        self.choose_exclusion_file_button.connect(
            "clicked", self.choose_exclusion
        )
        exclude_row.append(self.choose_exclusion_file_button)
        self.choose_exclusion_folder_button = Gtk.Button(
            label=self.tr("choose_exclusion_folder")
        )
        self.choose_exclusion_folder_button.connect(
            "clicked", self.choose_exclusion_folder
        )
        exclude_row.append(self.choose_exclusion_folder_button)
        form.append(exclude_row)

        # Exclude list
        self.exclude_list = Gtk.ListBox()
        self.exclude_list.set_selection_mode(Gtk.SelectionMode.NONE)
        form.append(self.exclude_list)

        # Cancel and Save buttons
        buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.cancel_button = Gtk.Button(label=self.tr("cancel"))
        self.cancel_button.connect("clicked", lambda _b: self.show_processes())
        buttons.append(self.cancel_button)

        self.save_button = Gtk.Button(label=self.tr("save"))
        self.save_button.add_css_class("suggested-action")
        self.save_button.connect("clicked", self.save_process)
        buttons.append(self.save_button)
        page.append(buttons)
        return page

    @staticmethod
    def field_label(text):
        # Create a label for a form field with styling
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.add_css_class("heading")
        return label

    def on_interval_unit_changed(self, dropdown, _param):
        # Handles the change between days and hours
        selected_unit = dropdown.get_selected()
        if selected_unit not in (0, 1):
            return
        if selected_unit == self.interval_unit:
            return

        hours = self.get_interval_hours()
        self.interval_unit = selected_unit
        if selected_unit == 1:
            self.interval_spin.set_range(1, 365)
            self.interval_spin.set_value((hours + 23) // 24)
        else:
            self.interval_spin.set_range(1, 8760)
            self.interval_spin.set_value(hours)

    def get_interval_hours(self):
        # From hours to days, else hours
        value = int(self.interval_spin.get_value())
        return value * 24 if self.interval_unit == 1 else value

    def new_backup(self, *_args):
        # Resets the fields for a new backup process
        self.editing_id = None
        self.sources = []
        self.destination = ""
        self.excluded_paths = []
        self.name_entry.set_text("")
        self.refresh_sources()
        self.dest_label.set_text(self.tr("no_destination"))
        self.interval_unit = 0
        self.interval_unit_dropdown.set_selected(0)
        self.interval_spin.set_range(1, 8760)
        self.interval_spin.set_value(24)
        self.start_time_entry.set_text("09:00")
        self.exclude_entry.set_text("")
        self.refresh_exclusions()
        self.editor_heading.set_text(self.tr("new_backup"))
        self.stack.set_visible_child_name("editor")
        self.header_title.set_text(self.tr("app_title"))

    def edit_process(self, _button, process_id):
        # Load the data into fields to edit an EXISTING backup process
        process = self.find_process(process_id)
        if not process:
            return
        self.editing_id = process_id
        self.sources = list(
            process.get("sources")
            or ([process["source"]] if process.get("source") else [])
        )
        self.destination = process.get("destination", "")
        self.excluded_paths = list(process.get("exclude", []))
        self.name_entry.set_text(
            process.get("name", self.tr("backup_default_name"))
        )
        self.refresh_sources()
        self.dest_label.set_text(
            self.destination or self.tr("no_destination")
        )
        interval_hours = max(1, int(process.get("interval_hours", 24)))
        self.interval_unit = 1 if interval_hours % 24 == 0 else 0
        self.interval_unit_dropdown.set_selected(self.interval_unit)
        # Sets the spin button based on units (hours, days)
        if self.interval_unit == 1:
            self.interval_spin.set_range(1, 365)
            self.interval_spin.set_value(interval_hours // 24)
        else:
            self.interval_spin.set_range(1, 8760)
            self.interval_spin.set_value(interval_hours)
        self.start_time_entry.set_text(process.get("start_time", "09:00"))
        self.exclude_entry.set_text("")
        self.refresh_exclusions()
        heading = self.tr("edit_backup")
        self.editor_heading.set_text(heading)
        self.stack.set_visible_child_name("editor")
        self.header_title.set_text(self.tr("app_title"))

    def choose_folder(self, title, callback):
        # Opens system folder chooser and shows the selected folder
        dialog = Gtk.FileChooserNative.new(
            title,
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            self.tr("select"),
            self.tr("cancel"),
        )
        dialog.connect("response", callback)
        dialog.show()

    def choose_source(self, _button):
        # Opens system folder chooser for source selection and shows the selected folder
        self.choose_folder(
            self.tr("choose_source_title"), self.on_source_selected
        )

    def choose_destination(self, _button):
        # Opens system folder chooser for destination selection and shows the selected folder
        self.choose_folder(
            self.tr("choose_destination_title"), self.on_destination_selected
        )

    def on_source_selected(self, dialog, response):
        # Handles the response from the source folder chooser dialog
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file and file.get_path():
                source = os.path.realpath(file.get_path())
                if source not in self.sources:
                    self.sources.append(source)
                    self.refresh_sources()
        dialog.destroy()

    def refresh_sources(self):
        # Refreshes the list of source folders displayed in the editor
        child = self.source_list.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.source_list.remove(child)
            child = next_child

        if not self.sources:
            label = Gtk.Label(label=self.tr("no_source"))
            label.set_xalign(0)
            label.add_css_class("dim-label")
            self.source_list.append(label)
            return

        for source in self.sources:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            label = Gtk.Label(label=source)
            label.set_xalign(0)
            label.set_hexpand(True)
            label.set_wrap(True)
            label.set_selectable(True)
            row.append(label)
            button = Gtk.Button(label=self.tr("remove_source"))
            button.connect("clicked", self.remove_source, source)
            row.append(button)
            self.source_list.append(row)

    def remove_source(self, _button, source):
        # Removes a source folder from the list and refreshes the display
        self.sources = [path for path in self.sources if path != source]
        self.refresh_sources()

    def on_destination_selected(self, dialog, response):
        # Handles the response from the destination folder chooser dialog
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file and file.get_path():
                self.destination = file.get_path()
                self.dest_label.set_text(self.destination)
        dialog.destroy()

    def choose_exclusion(self, _button):
        # Opens system file chooser for exclusion selection and shows the selected file
        self.open_exclusion_chooser(Gtk.FileChooserAction.OPEN)

    def choose_exclusion_folder(self, _button):
        # Opens system folder chooser for exclusion selection and shows the selected folder
        self.open_exclusion_chooser(Gtk.FileChooserAction.SELECT_FOLDER)

    def open_exclusion_chooser(self, action):
        # Opens a file chooser dialog for selecting files or folders to exclude from the backup process
        dialog = Gtk.FileChooserNative.new(
            self.tr("choose_exclusion_title"),
            self,
            action,
            self.tr("exclude_action"),
            self.tr("cancel"),
        )
        dialog.connect("response", self.on_exclusion_selected)
        dialog.show()

    def on_exclusion_selected(self, dialog, response):
        # Only adds selected file or folder;
        # Must be inside one of the source folders and not already excluded
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            path = file.get_path() if file else None
            if path:
                if not self.sources:
                    self.show_error(self.tr("choose_source_first"))
                else:
                    relative = None
                    try:
                        for source in self.sources:
                            candidate = os.path.relpath(path, source)
                            if candidate != os.pardir and not candidate.startswith(
                                os.pardir + os.sep
                            ):
                                relative = candidate
                                break
                    except ValueError:
                        self.show_error(self.tr("exclusion_path_error"))
                    else:
                        if relative is None:
                            self.show_error(
                                self.tr("exclusion_inside_source")
                            )
                        elif relative not in self.excluded_paths:
                            self.excluded_paths.append(relative)
                            self.refresh_exclusions()
        dialog.destroy()

    def add_exclusion(self, _button):
        # Adds a relative path to the exclusion list if able to
        value = self.exclude_entry.get_text().strip()
        if not value:
            return
        normalized = os.path.normpath(value)
        if os.path.isabs(normalized) or normalized == os.pardir or normalized.startswith(
            os.pardir + os.sep
        ):
            self.show_error(self.tr("relative_path_error"))
            return
        if normalized not in self.excluded_paths:
            self.excluded_paths.append(normalized)
        self.exclude_entry.set_text("")
        self.refresh_exclusions()

    def refresh_exclusions(self):
        # Refreshes the list of excluded paths displayed in the editor
        child = self.exclude_list.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.exclude_list.remove(child)
            child = next_child

        for path in self.excluded_paths:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            label = Gtk.Label(label=path)
            label.set_xalign(0)
            label.set_hexpand(True)
            label.set_wrap(True)
            row.append(label)
            button = Gtk.Button(label=self.tr("remove"))
            button.connect("clicked", self.remove_exclusion, path)
            row.append(button)
            self.exclude_list.append(row)

    def remove_exclusion(self, _button, path):
        # Removes a relative path from the exclusion list and refreshes the display
        self.excluded_paths = [p for p in self.excluded_paths if p != path]
        self.refresh_exclusions()

    def save_process(self, _button):
        # Validates input fields and saves the backup process configuration
        name = (
            self.name_entry.get_text().strip()
            or self.tr("backup_default_name")
        )
        try:
            start_time = datetime.strptime(
                self.start_time_entry.get_text().strip(), "%H:%M"
            ).strftime("%H:%M")
        except ValueError:
            self.show_error(self.tr("invalid_start_time"))
            return
        if not self.sources or not self.destination:
            self.show_error(self.tr("choose_both_folders"))
            return

        sources = list(dict.fromkeys(os.path.realpath(path) for path in self.sources))
        destination = os.path.realpath(self.destination)
        if not os.path.isdir(destination) or any(
            not os.path.isdir(source) for source in sources
        ):
            self.show_error(self.tr("folders_must_exist"))
            return
        for index, source in enumerate(sources):
            try:
                common = os.path.commonpath([source, destination])
            except ValueError:
                common = None
            if common in (source, destination):
                self.show_error(self.tr("folders_not_nested"))
                return
            for other_source in sources[index + 1:]:
                try:
                    common = os.path.commonpath([source, other_source])
                except ValueError:
                    common = None
                if common in (source, other_source):
                    self.show_error(self.tr("sources_not_nested"))
                    return

        process = {
            "id": self.editing_id or os.urandom(8).hex(),
            "name": name,
            "sources": sources,
            "destination": destination,
            "interval_hours": self.get_interval_hours(),
            "start_time": start_time,
            "exclude": list(self.excluded_paths),
            "last_run": None,
            "next_run": self.first_scheduled_run(
                start_time
            ).isoformat(timespec="seconds"),
        }
        existing = self.find_process(process["id"])
        if existing:
            process["last_run"] = existing.get("last_run")
            process["paused"] = existing.get("paused", False)
            self.processes = [
                process if p.get("id") == process["id"] else p
                for p in self.processes
            ]
        else:
            process["paused"] = False
            self.processes.append(process)

        try:
            self.save_processes()
        except OSError as error:
            self.show_error(self.tr("save_error").format(error=error))
            return

        self.show_processes()
