# app/views/user_management_view.py

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from app.views.base_view import BaseView
import tkinter.ttk as ttk

class UserManagementView(BaseView):
    def __init__(self, master, controller, user_info):
        super().__init__(master, controller, user_info)
        self.selected_user_id = None
        
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Gestión de Usuarios", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        self.user_table = ttk.Treeview(self.table_frame, columns=("ID", "Nombre", "Rol", "Activo"), show="headings")
        self.user_table.heading("ID", text="ID")
        self.user_table.heading("Nombre", text="Nombre de Usuario")
        self.user_table.heading("Rol", text="Rol")
        self.user_table.heading("Activo", text="Activo")
        self.user_table.grid(row=0, column=0, sticky="nsew")
        
        self.user_table.bind("<<TreeviewSelect>>", self._on_user_select)

        # --- BOTONES DE ACCIÓN ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=20)
        
        ctk.CTkButton(self.button_frame, text="Crear Usuario", command=self._create_user).pack(side="left", padx=10)
        ctk.CTkButton(self.button_frame, text="Editar Usuario", command=self._edit_user).pack(side="left", padx=10)
        ctk.CTkButton(self.button_frame, text="Desactivar", command=self._deactivate_user).pack(side="left", padx=10)
        ctk.CTkButton(self.button_frame, text="Activar", command=self._activate_user).pack(side="left", padx=10)
        ctk.CTkButton(self.button_frame, text="Volver al Panel", command=self._go_back_to_admin_panel).pack(side="left", padx=10)

    def load_users(self):
        for item in self.user_table.get_children():
            self.user_table.delete(item)
        users = self.controller.get_all_users_for_display()
        for user in users:
            self.user_table.insert("", "end", values=(
                user.get('id'), user.get('nombre_usuario'), 
                user.get('rol'), user.get('activo')
            ))

    def _on_user_select(self, event):
        selected_item = self.user_table.focus()
        if selected_item:
            self.selected_user_id = self.user_table.item(selected_item, 'values')[0]
        else:
            self.selected_user_id = None

    def _create_user(self):
        self._open_user_form_dialog(mode="create")

    def _edit_user(self):
        if not self.selected_user_id:
            CTkMessagebox(title="Error", message="Por favor, seleccione un usuario para editar.", icon="warning")
            return
        
        user_data = self.controller.get_user_by_id(self.selected_user_id)
        if user_data:
            self._open_user_form_dialog(mode="edit", user_data=user_data)
        else:
            CTkMessagebox(title="Error", message="No se pudo obtener la información del usuario.", icon="cancel")

    def _open_user_form_dialog(self, mode, user_data=None):
        dialog = ctk.CTkToplevel(self)
        title = "Crear Nuevo Usuario" if mode == "create" else "Editar Usuario"
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        dialog.grid_columnconfigure(1, weight=1)

        # Campos del formulario
        ctk.CTkLabel(dialog, text="Nombre de Usuario:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        username_entry = ctk.CTkEntry(dialog, width=250)
        username_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(dialog, text="Contraseña:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        password_entry = ctk.CTkEntry(dialog, show="*", width=250)
        password_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(dialog, text="Rol:").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        role_combo = ctk.CTkComboBox(dialog, values=["administrador", "cajero", "gerente"], width=250)
        role_combo.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        role_combo.set("cajero") # Rol por defecto

        if mode == "edit":
            username_entry.insert(0, user_data.get('nombre_usuario', ''))
            password_entry.configure(placeholder_text="Dejar en blanco para no cambiar")
            role_combo.set(user_data.get('rol', 'cajero'))

        message_label = ctk.CTkLabel(dialog, text="", text_color="red")
        message_label.grid(row=3, column=0, columnspan=2, pady=5)

        def on_submit():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combo.get()

            if mode == "create":
                success, message = self.controller.create_new_user(username, password, role)
            else: # mode == "edit"
                # Si el campo de contraseña está vacío, no la actualizamos pasando None
                password_to_update = password if password else None
                success, message = self.controller.update_existing_user(self.selected_user_id, username, password_to_update, role)

            if success:
                CTkMessagebox(title="Éxito", message=message, icon="check")
                self.load_users()
                dialog.destroy()
            else:
                message_label.configure(text=message)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        submit_button = ctk.CTkButton(button_frame, text="Guardar", command=on_submit)
        submit_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=dialog.destroy)
        cancel_button.pack(side="left", padx=10)

    def _deactivate_user(self):
        if not self.selected_user_id:
            CTkMessagebox(title="Error", message="Seleccione un usuario para desactivar.", icon="warning")
            return
        if self.controller.set_user_active_status(self.selected_user_id, False): 
            CTkMessagebox(title="Éxito", message=f"Usuario ID {self.selected_user_id} desactivado.", icon="check")
            self.load_users()
        else:
            CTkMessagebox(title="Error", message="Fallo al desactivar el usuario.", icon="cancel")

    def _activate_user(self):
        if not self.selected_user_id:
            CTkMessagebox(title="Error", message="Seleccione un usuario para activar.", icon="warning")
            return
        if self.controller.set_user_active_status(self.selected_user_id, True): 
            CTkMessagebox(title="Éxito", message=f"Usuario ID {self.selected_user_id} activado.", icon="check")
            self.load_users()
        else:
            CTkMessagebox(title="Error", message="Fallo al activar el usuario.", icon="cancel")

    def _go_back_to_admin_panel(self):
        self.master.show_admin_panel_frame(self.user_info)