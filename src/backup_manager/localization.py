import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


TRANSLATIONS = {
    "es": {
        "app_title": "Pating Backup Manager",
        "processes": "Procesos de copia",
        "new_backup": "Nueva copia",
        "name": "Nombre de la copia",
        "source": "Carpetas de origen",
        "add_source": "Añadir carpeta",
        "remove_source": "Quitar",
        "no_source": "No se ha seleccionado ninguna carpeta de origen",
        "pause": "Pausar",
        "resume": "Reanudar",
        "paused_status": "[Pausado]",
        "edit_backup": "Editar copia",
        "edit_action": "Editar",
        "remove_action": "Eliminar",
        "source_label": "Fuentes:",
        "destination_label": "Destino:",
        "frequency_label": "Frecuencia:",
        "start_time_label": "Hora de comienzo:",
        "exclusion_count": "{count} regla(s) de exclusión",
        "empty_process_list": (
            "No hay procesos de copia de seguridad.\n"
            "Crea una copia para empezar."
        ),
        "week_count": "{count} semana(s)",
        "day_count": "{count} día(s)",
        "fractional_days": "{days:.2f} días",
        "destination": "Destino de la copia",
        "interval": "Tiempo entre copias",
        "hours": "horas",
        "days": "días",
        "start_time": "Hora de inicio",
        "start_time_schedule_description": (
            "La hora establece la primera ejecución; después, se repite "
            "con el intervalo configurado."
        ),
        "start_time_placeholder": "HH:MM (formato de 24 horas)",
        "invalid_start_time": "Introduce una hora válida en formato HH:MM.",
        "exclude": "Excluir archivos y carpetas",
        "save": "Guardar proceso",
        "quit": "Salir de la aplicación",
        "quit_confirm_title": "¿Salir de la aplicación?",
        "quit_confirm_detail": "¿Seguro que quieres cerrar la aplicación?",
        "edit": "Editar",
        "remove": "Eliminar",
        "run_now": "Ejecutar ahora",
        "choose_folder": "Elegir carpeta",
        "change_to_light_theme": "Cambiar al tema claro",
        "change_to_dark_theme": "Cambiar al tema oscuro",
        "name_placeholder": "p. ej., Copia de documentos",
        "no_destination": "No se ha seleccionado el destino",
        "day_equivalence": "(24 horas = 1 día)",
        "exclude_description": (
            "Elige archivos o carpetas concretos que quieras omitir. "
            "Las rutas relativas se aplican a cada carpeta de origen."
        ),
        "exclude_placeholder": "Ruta relativa, p. ej., cache",
        "add_path": "Añadir ruta",
        "choose_exclusion_file": "Elegir archivo",
        "choose_exclusion_folder": "Elegir carpeta",
        "cancel": "Cancelar",
        "select": "Seleccionar",
        "exclude_action": "Excluir",
        "choose_source_title": "Elegir carpeta de origen",
        "choose_destination_title": "Elegir destino de la copia",
        "choose_exclusion_title": "Elegir archivo o carpeta para excluir",
        "choose_source_first": "Primero elige una carpeta de origen.",
        "exclusion_inside_source": (
            "La ruta excluida debe estar dentro de la carpeta de origen."
        ),
        "exclusion_path_error": "No se pudo usar esa ruta de exclusión.",
        "relative_path_error": (
            "Introduce una ruta relativa dentro de la carpeta de origen."
        ),
        "choose_both_folders": (
            "Elige tanto la carpeta de origen como la de destino."
        ),
        "folders_must_exist": "Las dos carpetas deben existir.",
        "folders_different": (
            "Las carpetas de origen y destino deben ser distintas."
        ),
        "folders_not_nested": (
            "La carpeta de origen y la de destino no pueden contenerse "
            "entre sí."
        ),
        "sources_not_nested": (
            "Las carpetas de origen no pueden contenerse entre sí."
        ),
        "history_tooltip": "Haz clic para ver el historial de copias",
        "history_title": "Historial de {name}",
        "history_empty": "Todavía no hay copias para esta tarea.",
        "history_entry": "{date} — {status} ({run_type})",
        "history_success": "Correcta",
        "history_failed": "Fallida",
        "history_scheduled": "Programada",
        "history_manual": "Manual",
        "history_unknown_type": "Tipo no registrado",
        "history_saved_to": "Guardada en: {path}",
        "history_location_unknown": "El destino de esta copia no se registró.",
        "history_error": "Error: {error}",
        "backup_default_name": "Copia",
        "close": "Cerrar",
        "remove_process_confirm": "¿Eliminar el proceso de copia «{name}»?",
        "remove_process_detail": (
            "Se eliminará la planificación guardada, no los archivos "
            "de las copias existentes."
        ),
        "backup_source_unconfigured": (
            "No se ha configurado la carpeta de origen o de destino."
        ),
        "backup_source_missing": (
            "La carpeta de origen o de destino ya no existe."
        ),
        "backup_paths_overlap": (
            "Las carpetas de origen y destino no pueden contenerse entre sí."
        ),
        "backup_sources_overlap": (
            "Las carpetas de origen seleccionadas no pueden contenerse "
            "entre sí."
        ),
        "save_schedule_error": (
            "No se pudo guardar la planificación de la copia: {error}"
        ),
        "backup_failed": "Error al realizar la copia: {error}",
        "backup_completed": "Copia completada correctamente.",
        "backup_completed_location": "Guardada en: {path}",
        "save_error": "No se pudo guardar el proceso de copia: {error}",
        "preferences_save_error": (
            "No se pudieron guardar las preferencias: {error}"
        ),
    },
    "en": {
        "app_title": "Pating Backup Manager",
        "processes": "Backup Processes",
        "new_backup": "New Backup",
        "name": "Backup name",
        "source": "Source folders",
        "add_source": "Add folder",
        "remove_source": "Remove",
        "no_source": "No source folders selected",
        "pause": "Pause",
        "resume": "Resume",
        "paused_status": "[Paused]",
        "edit_backup": "Edit Backup",
        "edit_action": "Edit",
        "remove_action": "Remove",
        "source_label": "Sources:",
        "destination_label": "Destination:",
        "frequency_label": "Frequency:",
        "start_time_label": "Start time:",
        "exclusion_count": "{count} exclusion rule(s)",
        "empty_process_list": (
            "No backup processes yet.\n"
            "Create a backup to get started."
        ),
        "week_count": "{count} week(s)",
        "day_count": "{count} day(s)",
        "fractional_days": "{days:.2f} days",
        "destination": "Backup destination",
        "interval": "Time between backups",
        "hours": "hours",
        "days": "days",
        "start_time": "Start time",
        "start_time_schedule_description": (
            "This sets the first run; later backups repeat at the configured "
            "interval."
        ),
        "start_time_placeholder": "HH:MM (24-hour format)",
        "invalid_start_time": "Enter a valid time in HH:MM format.",
        "exclude": "Exclude files and folders",
        "save": "Save Backup Process",
        "quit": "Quit application",
        "quit_confirm_title": "Quit application?",
        "quit_confirm_detail": "Are you sure you want to close the application?",
        "edit": "Edit",
        "remove": "Remove",
        "run_now": "Run now",
        "choose_folder": "Choose folder",
        "change_to_light_theme": "Change to light theme",
        "change_to_dark_theme": "Change to dark theme",
        "name_placeholder": "e.g. Documents backup",
        "no_destination": "No destination selected",
        "day_equivalence": "(24 hours = 1 day)",
        "exclude_description": (
            "Choose specific files or folders to skip. Exclusions are "
            "stored as relative paths applied to each source folder."
        ),
        "exclude_placeholder": "Relative path, e.g. cache",
        "add_path": "Add path",
        "choose_exclusion_file": "Choose file",
        "choose_exclusion_folder": "Choose folder",
        "cancel": "Cancel",
        "select": "Select",
        "exclude_action": "Exclude",
        "choose_source_title": "Choose Source Folder",
        "choose_destination_title": "Choose Backup Destination",
        "choose_exclusion_title": "Choose a file or folder to exclude",
        "choose_source_first": "Choose a source folder first.",
        "exclusion_inside_source": (
            "The excluded path must be inside the source folder."
        ),
        "exclusion_path_error": "Could not use that exclusion path.",
        "relative_path_error": (
            "Enter a relative path inside the source folder."
        ),
        "choose_both_folders": (
            "Choose both a source folder and destination."
        ),
        "folders_must_exist": "Both folders must exist.",
        "folders_different": (
            "Source and destination must be different folders."
        ),
        "folders_not_nested": (
            "Source and destination cannot contain one another."
        ),
        "sources_not_nested": (
            "Source folders cannot contain one another."
        ),
        "history_tooltip": "Click to view backup history",
        "history_title": "History for {name}",
        "history_empty": "There are no backups for this task yet.",
        "history_entry": "{date} — {status} ({run_type})",
        "history_success": "Successful",
        "history_failed": "Failed",
        "history_scheduled": "Scheduled",
        "history_manual": "Manual",
        "history_unknown_type": "Type not recorded",
        "history_saved_to": "Saved to: {path}",
        "history_location_unknown": "The destination for this backup was not recorded.",
        "history_error": "Error: {error}",
        "backup_default_name": "Backup",
        "close": "Close",
        "remove_process_confirm": "Remove backup process “{name}”?",
        "remove_process_detail": (
            "This removes the saved schedule, not files from existing backups."
        ),
        "backup_source_unconfigured": (
            "The source or destination folder is not configured."
        ),
        "backup_source_missing": (
            "The source or destination folder no longer exists."
        ),
        "backup_paths_overlap": (
            "Source and destination cannot contain one another."
        ),
        "backup_sources_overlap": (
            "Selected source folders cannot contain one another."
        ),
        "save_schedule_error": "Could not save backup schedule: {error}",
        "backup_failed": "Backup failed: {error}",
        "backup_completed": "Backup completed successfully.",
        "backup_completed_location": "Saved to: {path}",
        "save_error": "Could not save backup process: {error}",
        "preferences_save_error": "Could not save preferences: {error}",
    },
    "gl": {
        "app_title": "Pating Backup Manager",
        "processes": "Procesos de copia",
        "new_backup": "Nova copia",
        "name": "Nome da copia",
        "source": "Cartafoles de orixe",
        "add_source": "Engadir cartafol",
        "remove_source": "Retirar",
        "no_source": "Non hai cartafoles de orixe seleccionados",
        "pause": "Pausar",
        "resume": "Retomar",
        "paused_status": "[Pausado]",
        "edit_backup": "Editar copia",
        "edit_action": "Editar",
        "remove_action": "Eliminar",
        "source_label": "Orixes:",
        "destination_label": "Destino:",
        "frequency_label": "Frecuencia:",
        "start_time_label": "Hora de inicio:",
        "exclusion_count": "{count} regra(s) de exclusión",
        "empty_process_list": (
            "Aínda non hai procesos de copia.\n"
            "Crea unha copia para comezar."
        ),
        "week_count": "{count} semana(s)",
        "day_count": "{count} día(s)",
        "fractional_days": "{days:.2f} días",
        "destination": "Destino da copia",
        "interval": "Tempo entre copias",
        "hours": "horas",
        "days": "días",
        "start_time": "Hora de inicio",
        "start_time_schedule_description": (
            "A hora establece a primeira execución; despois, repítese "
            "co intervalo configurado."
        ),
        "start_time_placeholder": "HH:MM (formato de 24 horas)",
        "invalid_start_time": "Introduce unha hora válida no formato HH:MM.",
        "exclude": "Excluir ficheiros e cartafoles",
        "save": "Gardar tarefa",
        "quit": "Saír da aplicación",
        "quit_confirm_title": "Saír da aplicación?",
        "quit_confirm_detail": "Tes a certeza de que queres pechar a aplicación?",
        "edit": "Editar",
        "remove": "Retirar",
        "run_now": "Executar agora",
        "choose_folder": "Escoller cartafol",
        "change_to_light_theme": "Cambiar ao tema claro",
        "change_to_dark_theme": "Cambiar ao tema escuro",
        "name_placeholder": "p.ex., Copia de documentos",
        "no_destination": "Non se seleccionou o destino",
        "day_equivalence": "(24 horas = 1 día)",
        "exclude_description": (
            "Escolle ficheiros ou cartafoles concretos para omitir. "
            "As rutas relativas aplícanse a cada cartafol de orixe."
        ),
        "exclude_placeholder": "Ruta relativa, p.ex., cache",
        "add_path": "Engadir ruta",
        "choose_exclusion_file": "Escoller ficheiro",
        "choose_exclusion_folder": "Escoller cartafol",
        "cancel": "Cancelar",
        "select": "Seleccionar",
        "exclude_action": "Excluir",
        "choose_source_title": "Escoller cartafol de orixe",
        "choose_destination_title": "Escoller destino da copia",
        "choose_exclusion_title": "Escoller ficheiro ou cartafol para excluír",
        "choose_source_first": "Escolle primeiro un cartafol de orixe.",
        "exclusion_inside_source": (
            "A ruta excluída debe estar dentro do cartafol de orixe."
        ),
        "exclusion_path_error": "Non se puido usar esa ruta de exclusión.",
        "relative_path_error": (
            "Introduce unha ruta relativa dentro do cartafol de orixe."
        ),
        "choose_both_folders": (
            "Escolle tanto o cartafol de orixe como o de destino."
        ),
        "folders_must_exist": "Os dous cartafoles deben existir.",
        "folders_different": (
            "Os cartafoles de orixe e destino deben ser distintos."
        ),
        "folders_not_nested": (
            "O cartafol de orixe e o de destino non poden conterse entre si."
        ),
        "sources_not_nested": (
            "Os cartafoles de orixe non poden conterse entre si."
        ),
        "history_tooltip": "Preme para ver o historial das copias",
        "history_title": "Historial de {name}",
        "history_empty": "Aínda non hai copias para esta tarefa.",
        "history_entry": "{date} — {status} ({run_type})",
        "history_success": "Correcta",
        "history_failed": "Fallida",
        "history_scheduled": "Programada",
        "history_manual": "Manual",
        "history_unknown_type": "Tipo non rexistrado",
        "history_saved_to": "Gardada en: {path}",
        "history_location_unknown": "Non se rexistrou o destino desta copia.",
        "history_error": "Erro: {error}",
        "backup_default_name": "Copia",
        "close": "Pechar",
        "remove_process_confirm": "Queres retirar o proceso de copia «{name}»?",
        "remove_process_detail": (
            "Retírase a planificación gardada, non os ficheiros "
            "das copias existentes."
        ),
        "backup_source_unconfigured": (
            "Non se configurou o cartafol de orixe ou o de destino."
        ),
        "backup_source_missing": (
            "O cartafol de orixe ou o de destino xa non existe."
        ),
        "backup_paths_overlap": (
            "Os cartafoles de orixe e destino non poden conterse entre si."
        ),
        "backup_sources_overlap": (
            "Os cartafoles de orixe seleccionados non poden conterse "
            "entre si."
        ),
        "save_schedule_error": (
            "Non se puido gardar a planificación da copia: {error}"
        ),
        "backup_failed": "Produciuse un erro ao facer a copia: {error}",
        "backup_completed": "A copia completouse correctamente.",
        "backup_completed_location": "Gardada en: {path}",
        "save_error": "Non se puido gardar a tarefa de copia: {error}",
        "preferences_save_error": (
            "Non se puideron gardar as preferencias: {error}"
        ),
    },
    "pt-PT": {
        "app_title": "Pating Backup Manager",
        "processes": "Tarefas de cópia",
        "new_backup": "Nova cópia",
        "name": "Nome da cópia",
        "source": "Pastas de origem",
        "add_source": "Adicionar pasta",
        "remove_source": "Remover",
        "no_source": "Nenhuma pasta de origem selecionada",
        "pause": "Pausar",
        "resume": "Retomar",
        "paused_status": "[Pausado]",
        "edit_backup": "Editar cópia",
        "edit_action": "Editar",
        "remove_action": "Remover",
        "source_label": "Origens:",
        "destination_label": "Destino:",
        "frequency_label": "Frequência:",
        "start_time_label": "Hora de início:",
        "exclusion_count": "{count} regra(s) de exclusão",
        "empty_process_list": (
            "Ainda não existem tarefas de cópia.\n"
            "Crie uma cópia para começar."
        ),
        "week_count": "{count} semana(s)",
        "day_count": "{count} dia(s)",
        "fractional_days": "{days:.2f} dias",
        "destination": "Destino da cópia",
        "interval": "Intervalo entre cópias",
        "hours": "horas",
        "days": "dias",
        "start_time": "Hora de início",
        "start_time_schedule_description": (
            "A hora define a primeira execução; depois, repete-se "
            "com o intervalo configurado."
        ),
        "start_time_placeholder": "HH:MM (formato de 24 horas)",
        "invalid_start_time": "Introduza uma hora válida no formato HH:MM.",
        "exclude": "Excluir ficheiros e pastas",
        "save": "Guardar tarefa",
        "quit": "Sair da aplicação",
        "quit_confirm_title": "Sair da aplicação?",
        "quit_confirm_detail": "Tem a certeza de que pretende fechar a aplicação?",
        "edit": "Editar",
        "remove": "Remover",
        "run_now": "Executar agora",
        "choose_folder": "Escolher pasta",
        "change_to_light_theme": "Mudar para o tema claro",
        "change_to_dark_theme": "Mudar para o tema escuro",
        "name_placeholder": "p. ex., Cópia de documentos",
        "no_destination": "Nenhum destino selecionado",
        "day_equivalence": "(24 horas = 1 dia)",
        "exclude_description": (
            "Escolha ficheiros ou pastas específicos a ignorar. "
            "Os caminhos relativos aplicam-se a cada pasta de origem."
        ),
        "exclude_placeholder": "Caminho relativo, p. ex., cache",
        "add_path": "Adicionar caminho",
        "choose_exclusion_file": "Escolher ficheiro",
        "choose_exclusion_folder": "Escolher pasta",
        "cancel": "Cancelar",
        "select": "Selecionar",
        "exclude_action": "Excluir",
        "choose_source_title": "Escolher pasta de origem",
        "choose_destination_title": "Escolher destino da cópia",
        "choose_exclusion_title": "Escolher ficheiro ou pasta a excluir",
        "choose_source_first": "Escolha primeiro uma pasta de origem.",
        "exclusion_inside_source": (
            "O caminho excluído tem de estar dentro da pasta de origem."
        ),
        "exclusion_path_error": "Não foi possível utilizar esse caminho.",
        "relative_path_error": (
            "Introduza um caminho relativo dentro da pasta de origem."
        ),
        "choose_both_folders": (
            "Escolha a pasta de origem e o destino."
        ),
        "folders_must_exist": "As duas pastas têm de existir.",
        "folders_different": (
            "As pastas de origem e destino têm de ser diferentes."
        ),
        "folders_not_nested": (
            "A pasta de origem e o destino não podem conter-se mutuamente."
        ),
        "sources_not_nested": (
            "As pastas de origem não podem conter-se mutuamente."
        ),
        "history_tooltip": "Clique para ver o histórico das cópias",
        "history_title": "Histórico de {name}",
        "history_empty": "Ainda não existem cópias para esta tarefa.",
        "history_entry": "{date} — {status} ({run_type})",
        "history_success": "Concluída",
        "history_failed": "Falhada",
        "history_scheduled": "Agendada",
        "history_manual": "Manual",
        "history_unknown_type": "Tipo não registado",
        "history_saved_to": "Guardada em: {path}",
        "history_location_unknown": "O destino desta cópia não foi registado.",
        "history_error": "Erro: {error}",
        "backup_default_name": "Cópia",
        "close": "Fechar",
        "remove_process_confirm": "Remover o processo de cópia «{name}»?",
        "remove_process_detail": (
            "Esta ação remove o agendamento guardado, não os ficheiros "
            "das cópias existentes."
        ),
        "backup_source_unconfigured": (
            "A pasta de origem ou de destino não está configurada."
        ),
        "backup_source_missing": (
            "A pasta de origem ou de destino já não existe."
        ),
        "backup_paths_overlap": (
            "As pastas de origem e destino não podem conter-se mutuamente."
        ),
        "backup_sources_overlap": (
            "As pastas de origem selecionadas não podem conter-se "
            "mutuamente."
        ),
        "save_schedule_error": (
            "Não foi possível guardar o agendamento da cópia: {error}"
        ),
        "backup_failed": "Falha ao criar a cópia: {error}",
        "backup_completed": "Cópia concluída com sucesso.",
        "backup_completed_location": "Guardada em: {path}",
        "save_error": "Não foi possível guardar a tarefa de cópia: {error}",
        "preferences_save_error": (
            "Não foi possível guardar as preferências: {error}"
        ),
    },
}


class LocalizationMixin:
    def tr(self, key, english=None):
        # If English, returns the English translation; else, returns the translation for the current language; if it's not found, goes back to English
        if english is not None:
            if self.language == "es":
                return key
            if self.language == "en":
                return english
            for translation_key, english_value in self.translations["en"].items():
                if english_value == english:
                    return self.translations[self.language].get(
                        translation_key,
                        english,
                    )
            return english
        return self.translations[self.language].get(
            key,
            self.translations["en"].get(key, key)
        )

    def on_language_changed(self, dropdown, _param):
        # Updates the current language based on the dropdown selection and refreshes the UI texts accordingly
        language_codes = tuple(self.translations)
        selected = dropdown.get_selected()
        if selected < 0 or selected >= len(language_codes):
            return
        self.language = language_codes[selected]
        try:
            self.save_preferences()
        except OSError as error:
            self.show_error(
                self.tr("preferences_save_error").format(error=error)
            )
        self.refresh_texts()

    def refresh_texts(self):
        self.set_title(self.tr("app_title"))
        self.header_title.set_text(self.tr("app_title"))
        self.update_theme_button()
        self.quit_menu.remove_all()
        self.quit_menu.append(self.tr("quit"), "app.quit")
        self.processes_heading.set_text(self.tr("processes"))
        self.new_backup_button.set_label(self.tr("new_backup"))

        heading = (
            self.tr("edit_backup")
            if self.editing_id
            else self.tr("new_backup")
        )
        self.editor_heading.set_text(heading)
        for key, label in self.editor_labels.items():
            label.set_text(self.tr(key))
        self.name_entry.set_placeholder_text(self.tr("name_placeholder"))
        self.destination_button.set_label(self.tr("choose_folder"))
        self.refresh_sources()
        self.source_button.set_label(self.tr("add_source"))
        self.dest_label.set_text(
            self.destination or self.tr("no_destination")
        )
        self.day_equivalence_label.set_text(self.tr("day_equivalence"))
        selected_unit = self.interval_unit
        self.interval_unit_dropdown.set_model(
            Gtk.StringList.new([self.tr("hours"), self.tr("days")])
        )
        if selected_unit in (0, 1):
            self.interval_unit_dropdown.set_selected(selected_unit)
        self.start_time_entry.set_placeholder_text(
            self.tr("start_time_placeholder")
        )
        self.start_time_description.set_text(
            self.tr("start_time_schedule_description")
        )
        self.exclude_description.set_text(self.tr("exclude_description"))
        self.exclude_entry.set_placeholder_text(self.tr("exclude_placeholder"))
        self.choose_exclusion_file_button.set_label(
            self.tr("choose_exclusion_file")
        )
        self.choose_exclusion_folder_button.set_label(
            self.tr("choose_exclusion_folder")
        )
        self.cancel_button.set_label(self.tr("cancel"))
        self.save_button.set_label(self.tr("save"))
        self.refresh_exclusions()

        self.refresh_process_list()

    def toggle_theme(self, _button):
        self.dark_theme = not self.dark_theme
        self.set_dark_theme_preference(self.dark_theme)

        try:
            self.save_preferences()
        except OSError as error:
            self.show_error(
                self.tr("preferences_save_error").format(error=error)
            )
        self.update_theme_button()

    def update_theme_button(self):
        if self.dark_theme:
            self.theme_button.set_icon_name(
                "weather-clear-symbolic"
            )
            self.theme_button.set_tooltip_text(
                self.tr("change_to_light_theme")
            )
        else:
            self.theme_button.set_icon_name(
                "weather-clear-night-symbolic"
            )
            self.theme_button.set_tooltip_text(
                self.tr("change_to_dark_theme")
            )
