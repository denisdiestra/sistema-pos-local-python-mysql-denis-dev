# app/models/product_model.py

import mysql.connector 
from app.database.db_connection import get_db_connection

class ProductModel:
    """
    Gestiona las operaciones de base de datos relacionadas con los productos.
    """
    def __init__(self):
        self.db = get_db_connection()
        # === MEJORA: La conexión se establece una vez al inicio de la app, no aquí. ===
        self.db.connect()
        self._create_product_table() 

    def _create_product_table(self):
        """Crea la tabla de productos si no existe (para MySQL/MariaDB)."""
        # === MEJORA: No se necesita conectar/desconectar aquí, se asume conexión activa. ===
        try:
            query = '''
                CREATE TABLE IF NOT EXISTS Productos (
                    id INT PRIMARY KEY AUTO_INCREMENT, 
                    codigo_barras VARCHAR(255) UNIQUE NOT NULL, 
                    nombre_producto VARCHAR(255) NOT NULL,
                    descripcion TEXT,
                    id_categoria INT NOT NULL,
                    precio_venta DECIMAL(10, 2) NOT NULL, 
                    costo_unitario DECIMAL(10, 2) NOT NULL,
                    stock_actual INT NOT NULL,
                    stock_minimo INT NOT NULL,
                    unidad_medida VARCHAR(50) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT TRUE, 
                    FOREIGN KEY (id_categoria) REFERENCES Categorias(id)
                )
            '''
            self.db.execute_query(query)
            print("Tabla 'Productos' verificada/creada.")
        except Exception as e:
            print(f"Error al verificar/crear tabla 'Productos': {e}")

    def create_product(self, barcode, name, description, id_category, price, cost, stock, min_stock, unit):
        """
        Crea un nuevo producto en la base de datos.
        Retorna True si el producto fue creado, False en caso contrario.
        """
        query = """
            INSERT INTO Productos (codigo_barras, nombre_producto, descripcion, id_categoria, 
                                   precio_venta, costo_unitario, stock_actual, stock_minimo, 
                                   unidad_medida)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """ 
        params = (barcode, name, description, id_category, price, cost, stock, min_stock, unit)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def get_all_products(self):
        """Obtiene todos los productos, incluyendo el nombre de su categoría."""
        query = """
            SELECT p.id, p.codigo_barras, p.nombre_producto, p.descripcion, 
                   p.id_categoria, 
                   c.nombre_categoria, 
                   p.precio_venta, p.costo_unitario, p.stock_actual, p.stock_minimo, p.unidad_medida, p.activo
            FROM Productos p
            LEFT JOIN Categorias c ON p.id_categoria = c.id
        """ 
        results = self.db.fetch_all(query) 
        return results if results else []

    def get_product_by_barcode(self, barcode):
        """Busca un producto por su código de barras."""
        query = """
            SELECT p.id, p.codigo_barras, p.nombre_producto, p.descripcion, 
                   p.id_categoria, 
                   c.nombre_categoria,
                   p.precio_venta, p.costo_unitario, p.stock_actual, p.stock_minimo, p.unidad_medida, p.activo
            FROM Productos p
            LEFT JOIN Categorias c ON p.id_categoria = c.id
            WHERE p.codigo_barras = %s
        """ 
        params = (barcode,)
        result = self.db.fetch_one(query, params) 
        return result

    def get_product_by_id(self, product_id):
        """Busca un producto por su ID."""
        query = """
            SELECT p.id, p.codigo_barras, p.nombre_producto, p.descripcion, 
                   p.id_categoria, 
                   c.nombre_categoria,
                   p.precio_venta, p.costo_unitario, p.stock_actual, p.stock_minimo, p.unidad_medida, p.activo
            FROM Productos p
            LEFT JOIN Categorias c ON p.id_categoria = c.id
            WHERE p.id = %s
        """ 
        params = (product_id,)
        result = self.db.fetch_one(query, params) 
        return result

    def update_product(self, product_id, barcode, name, description, category_id, price, cost, stock, min_stock, unit, active):
        """Actualiza los datos de un producto existente."""
        query = """
            UPDATE Productos
            SET codigo_barras = %s, nombre_producto = %s, descripcion = %s, id_categoria = %s,
                precio_venta = %s, costo_unitario = %s, stock_actual = %s, stock_minimo = %s,
                unidad_medida = %s, activo = %s, ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id = %s
        """ 
        params = (barcode, name, description, category_id, price, cost, stock, min_stock, unit, active, product_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def update_product_stock(self, product_id, new_stock):
        """Actualiza solo el stock de un producto."""
        query = "UPDATE Productos SET stock_actual = %s, ultima_actualizacion = CURRENT_TIMESTAMP WHERE id = %s" 
        params = (new_stock, product_id)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def deactivate_product(self, product_id): # === MEJORA: Renombrado de 'delete_product' a 'deactivate_product' ===
        """Desactiva (no elimina físicamente) un producto, marcándolo como inactivo."""
        query = "UPDATE Productos SET activo = FALSE, ultima_actualizacion = CURRENT_TIMESTAMP WHERE id = %s" 
        params = (product_id,)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1

    def activate_product(self, product_id):
        """Marca un producto como activo."""
        query = "UPDATE Productos SET activo = TRUE, ultima_actualizacion = CURRENT_TIMESTAMP WHERE id = %s" 
        params = (product_id,)
        rows_affected = self.db.execute_query(query, params)
        return rows_affected == 1