# app/views/dashboard_view.py

import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    """
    Vista del panel principal/dashboard después de un inicio de sesión exitoso.
    """
    def __init__(self, master, user_controller, user_info):
        super().__init__(master)
        self.master = master # Referencia a MainAppView
        self.user_controller = user_controller # El UserController
        self.user_info = user_info # Información del usuario autenticado (ID, nombre, rol)

        self._create_widgets()

    def _create_widgets(self):
        # Configurar la rejilla del frame para centrar y expandir
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        welcome_label = ctk.CTkLabel(self, text=f"Bienvenido, {self.user_info['nombre_usuario']} ({self.user_info['rol']})",
                                     font=("Arial", 28, "bold"))
        welcome_label.grid(row=1, column=1, pady=20, sticky="nsew")

        # Botón para ir al panel de administración (solo si es administrador)
        if self.user_info['rol'] == 'administrador':
            from app.views.admin_panel_view import AdminPanelView # Importación tardía
            admin_button = ctk.CTkButton(self, text="Panel de Administración", 
                                        command=lambda: self.master.show_admin_panel_frame(self.user_info))
            admin_button.grid(row=2, column=1, pady=10)

        # Botón de Cerrar Sesión
        logout_button = ctk.CTkButton(self, text="Cerrar Sesión", command=self._on_logout)
        logout_button.grid(row=3, column=1, pady=20)

    def _on_logout(self):
        """
        Maneja el evento de clic en el botón de cerrar sesión.
        Vuelve a la vista de inicio de sesión.
        """
        print("Cerrando sesión...")
        from app.views.login_view import LoginView # Importación tardía para evitar circular
        self.master.show_frame(LoginView, self.user_controller) # Volver a la vista de login