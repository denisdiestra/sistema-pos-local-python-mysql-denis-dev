# app/controllers/category_controller.py

from app.models.category_model import CategoryModel
from app.controllers.base_controller import BaseController

class CategoryController(BaseController):
    """
    Controlador para la lógica de negocio de las categorías.
    """
    def __init__(self):
        super().__init__()
        self.category_model = CategoryModel()

    def get_all_categories(self):
        """Obtiene todas las categorías para mostrarlas en la vista."""
        return self.category_model.get_all_categories()

    def get_category_by_id(self, category_id):
        """Busca una categoría por su ID."""
        return self.category_model.get_category_by_id(category_id)

    def add_category(self, name, description=""):
        """
        Añade una nueva categoría. Retorna (bool, mensaje).
        """
        if not name:
            return False, "El nombre de la categoría es obligatorio."

        if self.category_model.get_category_by_name(name):
            return False, f"La categoría '{name}' ya existe."
        
        if self.category_model.create_category(name, description):
            return True, "Categoría creada exitosamente."
        else:
            return False, "Error desconocido al crear la categoría."

    def update_category(self, category_id, new_name, new_description):
        """
        Actualiza una categoría. Retorna (bool, mensaje).
        """
        if not new_name:
            return False, "El nombre de la categoría no puede estar vacío."

        current_category = self.category_model.get_category_by_id(category_id)
        if not current_category:
            return False, "La categoría a actualizar no existe."

        # Verifica si el nuevo nombre ya está en uso por OTRA categoría
        existing_category = self.category_model.get_category_by_name(new_name)
        if existing_category and existing_category['id'] != category_id:
             return False, f"El nombre '{new_name}' ya está en uso."

        if self.category_model.update_category(category_id, new_name, new_description):
            return True, "Categoría actualizada exitosamente."
        else:
            return False, "Error desconocido al actualizar la categoría."

    def delete_category(self, category_id):
        """
        Elimina una categoría. Retorna (bool, mensaje).
        """
        try:
            # Primero, verificamos si hay productos asociados
            # (Esto requeriría un método en ProductModel como get_products_by_category_id)
            # Por ahora, confiamos en la restricción de la base de datos.
            if self.category_model.delete_category(category_id):
                return True, "Categoría eliminada exitosamente."
            else:
                return False, "No se pudo eliminar (ID no encontrado)."
        except Exception as e:
            print(f"Error al eliminar categoría: {e}")
            return False, "No se puede eliminar: hay productos asociados."