# app/models/user_model.py

import bcrypt
from app.database.db_connection import get_db_connection

class UserModel:
    """
    Gestiona las operaciones de base de datos relacionadas con los usuarios.
    """
    def __init__(self):
        self.db = get_db_connection()
        # === MEJORA: La conexión se establece una vez al inicio de la app, no aquí. ===
        self.db.connect()
        self._create_user_table()

    def _create_user_table(self):
        """Crea la tabla de usuarios si no existe."""
        # === MEJORA: No se necesita conectar/desconectar aquí, se asume conexión activa. ===
        try:
            query = '''
                CREATE TABLE IF NOT EXISTS Usuarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre_usuario VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    rol VARCHAR(50) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultima_sesion TIMESTAMP NULL,
                    activo BOOLEAN DEFAULT TRUE
                )
            '''
            self.db.execute_query(query)
            print("Tabla 'Usuarios' verificada/creada.")
        except Exception as e:
            print(f"Error al verificar/crear tabla 'Usuarios': {e}")

    def create_user(self, username, password, role="cajero"):
        """
        Crea un nuevo usuario en la base de datos con una contraseña hasheada.
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO Usuarios (nombre_usuario, password_hash, rol) VALUES (%s, %s, %s)"
        params = (username, hashed_password, role)
        
        try:
            rows_affected = self.db.execute_query(query, params)
            return rows_affected == 1
        except Exception as e:
            print(f"Error al crear usuario {username}: {e}")
            return False

    def get_user_by_username(self, username):
        """Busca un usuario por su nombre de usuario."""
        query = "SELECT id, nombre_usuario, password_hash, rol, activo FROM Usuarios WHERE nombre_usuario = %s" 
        params = (username,)
        return self.db.fetch_one(query, params)

    def get_user_by_id(self, user_id):
        """Busca un usuario por su ID."""
        query = "SELECT id, nombre_usuario, password_hash, rol, activo FROM Usuarios WHERE id = %s" 
        params = (user_id,)
        return self.db.fetch_one(query, params)

    def verify_password(self, username, password):
        """Verifica la contraseña de un usuario."""
        user = self.get_user_by_username(username) 
        if user and 'password_hash' in user and user['password_hash']:
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return user 
        return None

    def update_user_last_login(self, user_id):
        """Actualiza la marca de tiempo de la última sesión de un usuario."""
        query = "UPDATE Usuarios SET ultima_sesion = CURRENT_TIMESTAMP WHERE id = %s"
        params = (user_id,)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def update_user_username(self, user_id, new_username):
        """Actualiza el nombre de usuario de un usuario."""
        query = "UPDATE Usuarios SET nombre_usuario = %s WHERE id = %s"
        params = (new_username, user_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def update_user_password(self, user_id, hashed_password):
        """Actualiza la contraseña hasheada de un usuario."""
        query = "UPDATE Usuarios SET password_hash = %s WHERE id = %s"
        params = (hashed_password, user_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def update_user_role(self, user_id, new_role):
        """Actualiza el rol de un usuario."""
        query = "UPDATE Usuarios SET rol = %s WHERE id = %s"
        params = (new_role, user_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def set_user_active_status(self, user_id, is_active):
        """Establece el estado activo/inactivo de un usuario."""
        query = "UPDATE Usuarios SET activo = %s WHERE id = %s"
        params = (is_active, user_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def get_all_users(self):
        """Obtiene todos los usuarios (activos e inactivos)."""
        query = "SELECT id, nombre_usuario, rol, activo, fecha_creacion, ultima_sesion FROM Usuarios"
        users_data = self.db.fetch_all(query)
        return users_data if users_data else []