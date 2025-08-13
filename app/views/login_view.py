# app/views/login_view.py

import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    """
    Vista para la pantalla de inicio de sesión.
    Permite al usuario introducir su nombre de usuario y contraseña.
    """
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master # Referencia a la ventana principal (MainAppView)
        self.controller = controller # El UserController que gestionará la autenticación

        self._create_widgets()

    def _create_widgets(self):
        """
        Crea y posiciona los widgets de la interfaz de inicio de sesión.
        """
        # Configurar la rejilla del frame para centrar el contenido
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        # Frame contenedor para centrar los elementos de login
        login_frame = ctk.CTkFrame(self, fg_color="transparent")
        login_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        
        login_frame.grid_rowconfigure((0,1,2,3,4), weight=0) # Contenido no se expande verticalmente
        login_frame.grid_columnconfigure((0,1), weight=1) # Columnas para etiquetas y entradas

        # Título
        title_label = ctk.CTkLabel(login_frame, text="Inicio de Sesión", font=("Arial", 28, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Campo de Usuario
        username_label = ctk.CTkLabel(login_frame, text="Usuario:", font=("Arial", 16))
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Ingrese su usuario", width=250)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Campo de Contraseña
        password_label = ctk.CTkLabel(login_frame, text="Contraseña:", font=("Arial", 16))
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Ingrese su contraseña", show="*", width=250)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Mensaje de error/éxito
        self.message_label = ctk.CTkLabel(login_frame, text="", text_color="red", font=("Arial", 14))
        self.message_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Botón de Iniciar Sesión
        login_button = ctk.CTkButton(login_frame, text="Ingresar", command=self._on_login)
        login_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Asociar la tecla Enter al botón de login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self._on_login())

    def _on_login(self):
        """
        Maneja el evento de clic en el botón de iniciar sesión.
        Envía las credenciales al controlador para su autenticación.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.configure(text="Por favor, ingrese usuario y contraseña.")
            return

        user_info = self.controller.authenticate_user(username, password)

        if user_info:
            self.message_label.configure(text="Inicio de sesión exitoso!", text_color="green")
            print(f"Usuario {user_info['nombre_usuario']} ha iniciado sesión con rol: {user_info['rol']}")
            # Aquí, dependiendo del rol, podrías mostrar una vista diferente
            # Por ahora, vamos a un dummy "dashboard"
            from app.views.dashboard_view import DashboardView # Importación tardía para evitar circular
            self.master.show_frame(DashboardView, self.controller, user_info) # Pasa el user_controller y la info del usuario
        else:
            self.message_label.configure(text="Usuario o contraseña incorrectos.", text_color="red")
            self.password_entry.delete(0, ctk.END) # Limpiar campo de contraseña
            self.username_entry.focus_set() # Poner el foco en el campo de usuario