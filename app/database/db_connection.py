# app/database/db_connection.py

import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG

class DBConnection:
    """
    Clase para manejar la conexión y operaciones con la base de datos MySQL/MariaDB.
    Implementa un patrón Singleton para asegurar una única instancia de conexión.
    """
    _instance = None # Para el patrón Singleton
    _connection = None
    _cursor = None

    def __new__(cls):
        """
        Implementa el patrón Singleton para asegurar que solo exista una instancia
        de la conexión a la base de datos.
        """
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """
        Establece la conexión a la base de datos si no está ya establecida.
        """
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=DB_CONFIG['host'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    database=DB_CONFIG['database'],
                    port=DB_CONFIG['port']
                )
                if self._connection.is_connected():
                    # Usamos dictionary=True para que el cursor devuelva diccionarios en lugar de tuplas
                    # Esto simplifica el acceso a los datos por nombre de columna en los modelos
                    self._cursor = self._connection.cursor(dictionary=True, buffered=True) 
                    print(f"Conexión a la base de datos '{DB_CONFIG['database']}' establecida con éxito.")
                else:
                    print("No se pudo establecer la conexión a la base de datos.")
            except Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                self._connection = None # Asegurar que la conexión es None si falla
                self._cursor = None
        return self._connection

    def disconnect(self):
        """
        Cierra la conexión a la base de datos si está abierta.
        """
        if self._connection and self._connection.is_connected():
            self._cursor.close()
            self._connection.close()
            print("Conexión a la base de datos cerrada.")
            self._connection = None # Limpiar la referencia
            self._cursor = None

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE, CREATE TABLE).
        Retorna el número de filas afectadas.
        No usar para SELECT, usar fetch_one o fetch_all.
        """
        if not self._connection or not self._connection.is_connected():
            print("No hay conexión activa a la base de datos para ejecutar una consulta DML. Intentando reconectar...")
            if not self.connect():
                return None

        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            self._connection.commit() # Confirmar cambios para DML
            return self._cursor.rowcount # Retorna el número de filas afectadas
        except Error as e:
            print(f"Error al ejecutar la consulta DML: {e}")
            if self._connection:
                self._connection.rollback() # Revertir cambios en caso de error
            return None

    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna una única fila como diccionario.
        Retorna None si no se encuentra ninguna fila o hay un error.
        """
        if not self._connection or not self._connection.is_connected():
            print("No hay conexión activa a la base de datos para fetch_one. Intentando reconectar...")
            if not self.connect():
                return None
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            return self._cursor.fetchone() # Retorna una fila como diccionario (gracias a dictionary=True)
        except Error as e:
            print(f"Error al ejecutar fetch_one: {e}")
            return None

    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna todas las filas como una lista de diccionarios.
        Retorna una lista vacía si no se encuentran filas o hay un error.
        """
        if not self._connection or not self._connection.is_connected():
            print("No hay conexión activa a la base de datos para fetch_all. Intentando reconectar...")
            if not self.connect():
                return []
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            return self._cursor.fetchall() # Retorna todas las filas como lista de diccionarios
        except Error as e:
            print(f"Error al ejecutar fetch_all: {e}")
            return []

    def __del__(self):
        """
        Asegura que la conexión se cierre cuando el objeto es destruido.
        """
        self.disconnect()

# Función para obtener una instancia global de la conexión
def get_db_connection():
    return DBConnection()

# Ejemplo de uso (esto es solo para probar y se puede eliminar o comentar después)
if __name__ == "__main__":
    db = get_db_connection()
    if db.connect():
        

        db.disconnect()