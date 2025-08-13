# app/models/category_model.py

import mysql.connector 
from app.database.db_connection import get_db_connection

class CategoryModel:
    """
    Gestiona las operaciones de base de datos relacionadas con las categorías.
    """
    def __init__(self):
        self.db = get_db_connection()
        # === MEJORA: La conexión se establece una vez al inicio de la app, no aquí. ===
        self.db.connect() 
        self._create_category_table()

    def _create_category_table(self):
        """Crea la tabla de categorías si no existe (para MySQL/MariaDB)."""
        # === MEJORA: No se necesita conectar/desconectar aquí, se asume conexión activa. ===
        try:
            query = '''
                CREATE TABLE IF NOT EXISTS Categorias (
                    id INT PRIMARY KEY AUTO_INCREMENT, 
                    nombre_categoria VARCHAR(255) UNIQUE NOT NULL,
                    descripcion TEXT
                )
            '''
            self.db.execute_query(query)
            print("Tabla 'Categorias' verificada/creada.")
        except Exception as e:
            print(f"Error al verificar/crear tabla 'Categorias': {e}")

    def create_category(self, name, description=""):
        """Crea una nueva categoría."""
        query = "INSERT INTO Categorias (nombre_categoria, descripcion) VALUES (%s, %s)"
        params = (name, description)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def get_all_categories(self):
        """Obtiene todas las categorías."""
        query = "SELECT id, nombre_categoria, descripcion FROM Categorias"
        results = self.db.fetch_all(query) 
        return results if results else []

    def get_category_by_id(self, category_id):
        """Busca una categoría por su ID."""
        query = "SELECT id, nombre_categoria, descripcion FROM Categorias WHERE id = %s"
        params = (category_id,)
        result = self.db.fetch_one(query, params) 
        return result

    def get_category_by_name(self, category_name):
        """Busca una categoría por su nombre."""
        query = "SELECT id, nombre_categoria, descripcion FROM Categorias WHERE nombre_categoria = %s"
        params = (category_name,)
        result = self.db.fetch_one(query, params) 
        return result

    def update_category(self, category_id, new_name, new_description):
        """Actualiza una categoría existente."""
        query = "UPDATE Categorias SET nombre_categoria = %s, descripcion = %s WHERE id = %s"
        params = (new_name, new_description, category_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def delete_category(self, category_id):
        """Elimina una categoría por su ID."""
        # Advertencia: Esto podría fallar si hay productos que dependen de esta categoría (Foreign Key).
        # Una mejor estrategia podría ser un borrado lógico o impedir el borrado si hay productos asociados.
        query = "DELETE FROM Categorias WHERE id = %s"
        params = (category_id,)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1