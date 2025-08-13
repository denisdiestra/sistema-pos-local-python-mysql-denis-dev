# app/views/category_management_view.py

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.ttk as ttk

class CategoryManagementView(ctk.CTkFrame):
    def __init__(self, master, category_controller, user_controller, user_info):
        super().__init__(master)
        self.master = master
        self.category_controller = category_controller 
        self.user_controller = user_controller
        self.user_info = user_info
        
        self._create_widgets()
        self._load_categories()

    def _create_widgets(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(self, text="Gestión de Categorías", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=20, sticky="ew")

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.category_table = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Descripción"), show="headings")
        self.category_table.heading("ID", text="ID")
        self.category_table.heading("Nombre", text="Nombre Categoría")
        self.category_table.heading("Descripción", text="Descripción")
        self.category_table.column("ID", width=50, anchor="center")
        self.category_table.column("Nombre", width=250, anchor="w")
        self.category_table.column("Descripción", width=400, anchor="w")
        self.category_table.grid(row=0, column=0, sticky="nsew")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20)
        ctk.CTkButton(button_frame, text="Crear Categoría", command=self._open_create_dialog).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Editar Categoría", command=self._open_edit_dialog).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Eliminar", command=self._delete_selected_category).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Volver al Panel", command=self._go_back_to_admin_panel).pack(side="left", padx=5)

    def _load_categories(self):
        for item in self.category_table.get_children():
            self.category_table.delete(item)
        categories = self.category_controller.get_all_categories()
        for cat in categories:
            self.category_table.insert("", "end", values=(cat['id'], cat['nombre_categoria'], cat.get('descripcion', '')))

    def _open_create_dialog(self):
        self._show_form_dialog(mode="create")

    def _open_edit_dialog(self):
        selected_item = self.category_table.focus()
        if not selected_item:
            CTkMessagebox(title="Error", message="Seleccione una categoría para editar.", icon="warning")
            return
        
        category_id = self.category_table.item(selected_item, "values")[0]
        category_data = self.category_controller.get_category_by_id(category_id)
        if category_data:
            self._show_form_dialog(mode="edit", category_data=category_data)
        else:
            CTkMessagebox(title="Error", message="No se pudo obtener la información de la categoría.", icon="cancel")

    def _show_form_dialog(self, mode, category_data=None):
        dialog = ctk.CTkToplevel(self)
        title = "Crear Nueva Categoría" if mode == "create" else "Editar Categoría"
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(dialog, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        desc_entry = ctk.CTkEntry(dialog, width=250)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)

        if mode == "edit":
            name_entry.insert(0, category_data.get('nombre_categoria', ''))
            desc_entry.insert(0, category_data.get('descripcion', ''))

        message_label = ctk.CTkLabel(dialog, text="", text_color="red")
        message_label.grid(row=2, column=0, columnspan=2, pady=5)

        def on_submit():
            name = name_entry.get()
            description = desc_entry.get()

            if mode == "create":
                success, message = self.category_controller.add_category(name, description)
            else: # mode == "edit"
                category_id = category_data['id']
                success, message = self.category_controller.update_category(category_id, name, description)

            if success:
                CTkMessagebox(title="Éxito", message=message, icon="check")
                self._load_categories()
                dialog.destroy()
            else:
                message_label.configure(text=message)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Guardar", command=on_submit).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=dialog.destroy).pack(side="left", padx=10)

    def _delete_selected_category(self):
        selected_item = self.category_table.focus()
        if not selected_item:
            CTkMessagebox(title="Error", message="Seleccione una categoría para eliminar.", icon="warning")
            return
        
        values = self.category_table.item(selected_item, "values")
        category_id, category_name = values[0], values[1]
        
        msg = CTkMessagebox(title="Confirmar Eliminación", 
                            message=f"¿Está seguro de que desea eliminar la categoría '{category_name}'?",
                            icon="question", option_1="Cancelar", option_2="Eliminar")
        if msg.get() == "Eliminar":
            success, message = self.category_controller.delete_category(category_id)
            if success:
                CTkMessagebox(title="Éxito", message=message, icon="check")
                self._load_categories()
            else:
                CTkMessagebox(title="Error", message=message, icon="cancel")

    def _go_back_to_admin_panel(self):
        self.master.show_admin_panel_frame(self.user_info)