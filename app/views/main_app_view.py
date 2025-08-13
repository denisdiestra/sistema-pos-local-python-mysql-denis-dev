# app/views/main_app_view.py

import customtkinter as ctk
# === MEJORA: Centralizar la creación de controladores ===
from app.controllers.user_controller import UserController 
from app.controllers.product_controller import ProductController
from app.controllers.category_controller import CategoryController

class MainAppView(ctk.CTk):
    """
    Clase principal de la aplicación gráfica.
    Representa la ventana principal y maneja la navegación entre vistas.
    """
    def __init__(self):
        super().__init__()

        self.title("Sistema POS MiniMarket - Comas, Perú")
        self.geometry("1024x768") 
        self.minsize(800, 600) 
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue") 

        # === MEJORA: Instanciar todos los controladores aquí para que sean persistentes ===
        self.user_controller = UserController()
        self.product_controller = ProductController()
        self.category_controller = CategoryController()

        self.current_frame = None 
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.show_login_frame() 

    def _on_closing(self):
        print("Cerrando aplicación. Desconectando base de datos...")
        self.user_controller.disconnect_db() 
        self.destroy() 

    def show_frame(self, new_frame_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy() 
        
        # === MEJORA: Los controladores se pasan desde aquí ===
        self.current_frame = new_frame_class(self, *args, **kwargs) 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.current_frame.tkraise() 

    def show_login_frame(self):
        from app.views.login_view import LoginView
        # Pasa solo el controlador que necesita
        self.show_frame(LoginView, self.user_controller)

    def show_admin_panel_frame(self, user_info):
        from app.views.admin_panel_view import AdminPanelView
        # Pasa todos los controladores y la info del usuario al panel de admin
        self.show_frame(AdminPanelView, user_info, self.user_controller, self.product_controller, self.category_controller)