# app/views/base_view.py

import customtkinter as ctk

class BaseView(ctk.CTkFrame):
    """
    Clase base para todas las vistas de la aplicación.
    Proporciona una estructura común para las vistas de CustomTkinter.
    """
    def __init__(self, master, controller, user_info=None):
        super().__init__(master)
        self.master = master
        self.controller = controller # Controlador principal (ej. user_controller)
        self.user_info = user_info   # Información del usuario logueado (si aplica)

        # Configuración básica de la rejilla para las vistas derivadas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)