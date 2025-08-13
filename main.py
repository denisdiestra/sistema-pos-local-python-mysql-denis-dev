# main.py

import customtkinter as ctk
from app.views.main_app_view import MainAppView
from app.database.db_connection import get_db_connection

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # === MEJORA: Gestionar el ciclo de vida de la conexión explícitamente ===
    db = None
    try:
        # 1. Conectar a la base de datos al iniciar la app
        db = get_db_connection()
        db.connect()

        # 2. Iniciar la aplicación
        app = MainAppView() 
        app.mainloop()

    except Exception as e:
        print(f"Ha ocurrido un error en la aplicación: {e}")
    finally:
        # 3. Desconectar de la base de datos al cerrar la app
        if db:
            db.disconnect()
            print("Aplicación cerrada. Conexión a la base de datos finalizada.")