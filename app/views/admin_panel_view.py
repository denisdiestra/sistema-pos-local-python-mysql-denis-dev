# app/views/admin_panel_view.py

import customtkinter as ctk
from app.views.base_view import BaseView

# === MEJORA: Hereda de BaseView para estandarizar ===
class AdminPanelView(BaseView):
    """
    Panel de administración que navega a otras vistas de gestión.
    """
    # === MEJORA: Recibe los controladores en lugar de solo user_controller ===
    def __init__(self, master, user_info, user_controller, product_controller, category_controller):
        # BaseView no necesita todos los controladores, solo pasamos uno como referencia genérica
        super().__init__(master, user_controller, user_info)
        self.product_controller = product_controller
        self.category_controller = category_controller
        self._create_widgets()

    def _create_widgets(self):
        self.grid_rowconfigure((0,1,2,3,4,5), weight=0) # Centrar verticalmente
        self.grid_columnconfigure(0, weight=1)

        # Contenedor para los botones
        button_container = ctk.CTkFrame(self, fg_color="transparent")
        button_container.grid(row=1, column=0, rowspan=5, sticky="n")

        title_label = ctk.CTkLabel(self, text="Panel de Administración", font=("Arial", 28, "bold"))
        title_label.grid(row=0, column=0, pady=40)

        manage_users_button = ctk.CTkButton(button_container, text="Gestionar Usuarios", command=self._open_user_management, width=200, height=40)
        manage_users_button.pack(pady=10)

        manage_products_button = ctk.CTkButton(button_container, text="Gestionar Productos", command=self._open_product_management, width=200, height=40)
        manage_products_button.pack(pady=10)

        manage_categories_button = ctk.CTkButton(button_container, text="Gestionar Categorías", command=self._open_category_management, width=200, height=40)
        manage_categories_button.pack(pady=10)

        back_button = ctk.CTkButton(button_container, text="Volver al Dashboard", command=self._go_back_to_dashboard, width=200, height=40)
        back_button.pack(pady=(40, 10))

    def _open_user_management(self):
        from app.views.user_management_view import UserManagementView
        # Pasa el user_controller y la info
        self.master.show_frame(UserManagementView, self.controller, self.user_info)

    def _open_product_management(self):
        from app.views.product_management_view import ProductManagementView
        # === MEJORA: Pasa la instancia existente del product_controller ===
        self.master.show_frame(ProductManagementView, self.product_controller, self.controller, self.user_info)

    def _open_category_management(self):
        from app.views.category_management_view import CategoryManagementView
        # === MEJORA: Pasa la instancia existente del category_controller ===
        self.master.show_frame(CategoryManagementView, self.category_controller, self.controller, self.user_info)

    def _go_back_to_dashboard(self):
        from app.views.dashboard_view import DashboardView
        # Para volver al dashboard, solo necesitamos el user_controller y la info
        self.master.show_frame(DashboardView, self.controller, self.user_info)