# app/controllers/user_controller.py

from app.models.user_model import UserModel
from app.controllers.base_controller import BaseController
import bcrypt

class UserController(BaseController):
    """
    Controlador para gestionar la lógica de negocio de usuarios.
    Maneja la autenticación y las operaciones CRUD de usuarios.
    """
    def __init__(self):
        super().__init__()
        self.user_model = UserModel()

    def authenticate_user(self, username, password):
        """
        Autentica un usuario.
        Retorna el objeto de usuario (diccionario) si las credenciales son correctas y el usuario está activo, de lo contrario None.
        """
        user = self.user_model.verify_password(username, password)
        if user:
            # En MySQL, True es 1 y False es 0.
            if user.get('activo') == 1:
                self.user_model.update_user_last_login(user['id'])
                print(f"Usuario '{username}' autenticado correctamente. Rol: {user['rol']}")
                return user
            else:
                print(f"Error: Usuario '{username}' está inactivo.")
                return None
        print(f"Error de autenticación para '{username}': Usuario o contraseña incorrectos.")
        return None

    def get_user_by_id(self, user_id):
        """
        Obtiene los datos de un usuario por su ID.
        """
        return self.user_model.get_user_by_id(user_id)

    def create_new_user(self, username, password, role):
        """
        Crea un nuevo usuario en el sistema.
        Retorna una tupla (bool, str) indicando éxito y un mensaje.
        """
        if not username or not password or not role:
            return False, "Nombre, contraseña y rol son obligatorios."

        existing_user = self.user_model.get_user_by_username(username)
        if existing_user:
            return False, f"El nombre de usuario '{username}' ya existe."

        if self.user_model.create_user(username, password, role):
            return True, f"Usuario '{username}' creado exitosamente."
        else:
            return False, "Error desconocido al crear el usuario."

    def update_existing_user(self, user_id, new_username, new_password, new_role):
        """
        Actualiza la información de un usuario existente.
        Retorna una tupla (bool, str) indicando éxito y un mensaje.
        """
        user_data = self.user_model.get_user_by_id(user_id)
        if not user_data:
            return False, "Usuario no encontrado para actualizar."

        if new_username and new_username != user_data['nombre_usuario']:
            existing_user = self.user_model.get_user_by_username(new_username)
            if existing_user and existing_user['id'] != user_id:
                return False, f"El nombre de usuario '{new_username}' ya está en uso."
            self.user_model.update_user_username(user_id, new_username)

        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.user_model.update_user_password(user_id, hashed_password)

        if new_role and new_role != user_data['rol']:
            self.user_model.update_user_role(user_id, new_role)

        return True, "Usuario actualizado exitosamente."

    def get_all_users_for_display(self):
        """
        Obtiene una lista de todos los usuarios registrados, formateada para la visualización.
        """
        users = self.user_model.get_all_users()
        formatted_users = []
        if users:
            for user in users:
                formatted_user = {
                    'id': user.get('id'),
                    'nombre_usuario': user.get('nombre_usuario'),
                    'rol': user.get('rol'),
                    'activo': "Sí" if user.get('activo') == 1 else "No"
                }
                formatted_users.append(formatted_user)
        return formatted_users

    def set_user_active_status(self, user_id, is_active):
        """
        Método del controlador para cambiar el estado activo/inactivo de un usuario.
        """
        return self.user_model.set_user_active_status(user_id, is_active)

    def disconnect_db(self):
        """
        Desconecta la base de datos a través del modelo de usuario.
        """
        if self.user_model.db:
            self.user_model.db.disconnect()
        print("Controlador de Usuario: Desconexión de la BD finalizada.")