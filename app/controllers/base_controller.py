# app/controllers/base_controller.py

from app.database.db_connection import get_db_connection

class BaseController:
    """
    Controlador base para manejar funcionalidades comunes como la desconexión de la BD.
    """
    def __init__(self):
        self.db_connection = get_db_connection()

    def disconnect_db(self):
        """
        Cierra la conexión activa a la base de datos.
        Este método será llamado al cerrar la aplicación para asegurar una desconexión limpia.
        """
        self.db_connection.disconnect()
        print("Controlador base: Conexión a la BD cerrada al salir.")