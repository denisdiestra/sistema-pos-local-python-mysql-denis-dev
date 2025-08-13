# app/controllers/product_controller.py

from app.models.product_model import ProductModel
from app.models.category_model import CategoryModel
from app.controllers.base_controller import BaseController

class ProductController(BaseController):
    """
    Controlador para gestionar la lógica de negocio de productos e inventario.
    """
    def __init__(self):
        super().__init__()
        self.product_model = ProductModel()
        self.category_model = CategoryModel()

    def get_product_by_id(self, product_id):
        """Obtiene los datos de un producto por su ID."""
        return self.product_model.get_product_by_id(product_id)

    def add_product(self, barcode, name, description, category_name, price, cost, stock, min_stock, unit):
        """
        Añade un nuevo producto. Retorna (bool, mensaje).
        """
        if not all([barcode, name, category_name, price, cost, stock, min_stock, unit]):
            return False, "Todos los campos son obligatorios."
            
        category = self.category_model.get_category_by_name(category_name)
        if not category:
            self.category_model.create_category(category_name)
            category = self.category_model.get_category_by_name(category_name)
            if not category:
                return False, "Error crítico al crear/obtener la categoría."
        
        category_id = category['id']

        if self.product_model.get_product_by_barcode(barcode):
            return False, f"El código de barras '{barcode}' ya existe."
            
        if self.product_model.create_product(barcode, name, description, category_id, price, cost, stock, min_stock, unit):
            return True, f"Producto '{name}' añadido exitosamente."
        else:
            return False, "Error desconocido al añadir el producto."

    def update_product_details(self, product_id, barcode, name, description, category_name, price, cost, stock, min_stock, unit, active):
        """
        Actualiza los detalles de un producto. Retorna (bool, mensaje).
        """
        category = self.category_model.get_category_by_name(category_name)
        if not category:
            return False, f"La categoría '{category_name}' no existe."
        category_id = category['id']

        # Validar que el código de barras (si cambió) no esté en uso por OTRO producto
        existing_product = self.product_model.get_product_by_barcode(barcode)
        if existing_product and existing_product['id'] != product_id:
            return False, f"El código de barras '{barcode}' ya está en uso por otro producto."

        if self.product_model.update_product(product_id, barcode, name, description, category_id, price, cost, stock, min_stock, unit, active):
            return True, f"Producto '{name}' actualizado exitosamente."
        else:
            return False, "Fallo al actualizar el producto."

    def get_products_for_display(self):
        """
        Obtiene todos los productos para la vista.
        """
        products_raw = self.product_model.get_all_products()
        products_display = []
        for prod in products_raw:
            products_display.append({
                'id': prod['id'],
                'codigo_barras': prod['codigo_barras'],
                'nombre_producto': prod['nombre_producto'],
                'descripcion': prod['descripcion'],
                'categoria': prod.get('nombre_categoria', "Desconocida"),
                'precio_venta': prod['precio_venta'],
                'costo_unitario': prod['costo_unitario'],
                'stock_actual': prod['stock_actual'],
                'stock_minimo': prod['stock_minimo'],
                'unidad_medida': prod['unidad_medida'],
                'activo': prod['activo']
            })
        return products_display

    def remove_product(self, product_id):
        """Desactiva un producto (soft delete)."""
        return self.product_model.deactivate_product(product_id)
        
    def activate_product(self, product_id):
        """Activa un producto."""
        return self.product_model.activate_product(product_id)