# app/views/product_management_view.py

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.ttk as ttk
from app.controllers.product_controller import ProductController
from app.models.category_model import CategoryModel

class ProductManagementView(ctk.CTkFrame):
    def __init__(self, master, product_controller: ProductController, user_controller, user_info): 
        super().__init__(master)
        self.master = master
        self.product_controller = product_controller
        self.user_controller = user_controller 
        self.user_info = user_info 
        self.category_model = CategoryModel()

        self._create_widgets()
        self._load_products()

    def _create_widgets(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(self, text="Gestión de Productos", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=20, sticky="ew")

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ("ID", "Código Barras", "Nombre", "Stock", "Precio", "Categoría", "Activo")
        self.product_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.product_table.grid(row=0, column=0, sticky="nsew")
        
        for col in columns: self.product_table.heading(col, text=col)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20)
        ctk.CTkButton(button_frame, text="Crear Producto", command=self._open_create_product_dialog).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Editar Producto", command=self._open_edit_product_dialog).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Volver al Panel", command=self._go_back_to_admin_panel).pack(side="left", padx=5)

    def _load_products(self):
        for item in self.product_table.get_children(): self.product_table.delete(item)
        products = self.product_controller.get_products_for_display()
        for prod in products:
            self.product_table.insert("", "end", values=(
                prod['id'], prod['codigo_barras'], prod['nombre_producto'], 
                f"{prod['stock_actual']}", f"{prod['precio_venta']:.2f}", 
                prod['categoria'], "Sí" if prod['activo'] else "No"
            ))

    def _open_create_product_dialog(self):
        self._show_product_form_dialog(mode="create")

    def _open_edit_product_dialog(self):
        selected_item = self.product_table.focus()
        if not selected_item:
            CTkMessagebox(title="Error", message="Por favor, seleccione un producto para editar.", icon="warning")
            return
        
        product_id = self.product_table.item(selected_item, "values")[0]
        product_data = self.product_controller.get_product_by_id(product_id)
        if product_data:
            self._show_product_form_dialog(mode="edit", product_data=product_data)
        else:
            CTkMessagebox(title="Error", message="No se pudo obtener la información del producto.", icon="cancel")

    def _show_product_form_dialog(self, mode, product_data=None):
        dialog = ctk.CTkToplevel(self)
        title = "Crear Nuevo Producto" if mode == "create" else "Editar Producto"
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()

        # FORMULARIO
        labels = ["Código de Barras:", "Nombre:", "Descripción:", "Categoría:", "Precio Venta:", "Costo Unitario:", "Stock Actual:", "Stock Mínimo:", "Unidad de Medida:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ctk.CTkLabel(dialog, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if label_text == "Categoría:":
                # === CORRECCIÓN AQUÍ ===
                # Nos aseguramos de que solo nombres de categoría válidos (no nulos o vacíos) se añadan a la lista.
                all_cats = self.category_model.get_all_categories()
                valid_categories = [cat['nombre_categoria'] for cat in all_cats if cat and cat.get('nombre_categoria')]
                entry = ctk.CTkComboBox(dialog, values=valid_categories, width=250)
                if not valid_categories:
                    entry.set("No hay categorías") # Mensaje si no hay categorías
            
            elif label_text == "Unidad de Medida:":
                entry = ctk.CTkComboBox(dialog, values=["Unidad", "Kg", "Litro", "Paquete"], width=250)
            else:
                entry = ctk.CTkEntry(dialog, width=250)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[label_text] = entry
        
        if mode == "edit":
            entries["Código de Barras:"].insert(0, product_data.get('codigo_barras', ''))
            entries["Nombre:"].insert(0, product_data.get('nombre_producto', ''))
            entries["Descripción:"].insert(0, product_data.get('descripcion', ''))
            
            # Se asegura de que la categoría del producto a editar exista en la lista del combobox
            category_to_set = product_data.get('nombre_categoria')
            if category_to_set in valid_categories:
                entries["Categoría:"].set(category_to_set)

            entries["Precio Venta:"].insert(0, str(product_data.get('precio_venta', '')))
            entries["Costo Unitario:"].insert(0, str(product_data.get('costo_unitario', '')))
            entries["Stock Actual:"].insert(0, str(product_data.get('stock_actual', '')))
            entries["Stock Mínimo:"].insert(0, str(product_data.get('stock_minimo', '')))
            entries["Unidad de Medida:"].set(product_data.get('unidad_medida', ''))
            entries["Código de Barras:"].configure(state="disabled")

        message_label = ctk.CTkLabel(dialog, text="", text_color="red")
        message_label.grid(row=len(labels), column=0, columnspan=2, pady=5)
        
        def on_submit():
            try:
                # ... (la lógica de on_submit se mantiene igual) ...
                form_data = {
                    "barcode": entries["Código de Barras:"].get(),
                    "name": entries["Nombre:"].get(),
                    "description": entries["Descripción:"].get(),
                    "category_name": entries["Categoría:"].get(),
                    "price": float(entries["Precio Venta:"].get()),
                    "cost": float(entries["Costo Unitario:"].get()),
                    "stock": int(entries["Stock Actual:"].get()),
                    "min_stock": int(entries["Stock Mínimo:"].get()),
                    "unit": entries["Unidad de Medida:"].get(),
                }
            except (ValueError, TypeError):
                message_label.configure(text="Error: Precio, costo y stock deben ser números válidos.")
                return

            if form_data["category_name"] == "No hay categorías":
                message_label.configure(text="Error: Debe seleccionar o crear una categoría válida.")
                return

            if mode == "create":
                success, message = self.product_controller.add_product(**form_data)
            else: # mode == "edit"
                success, message = self.product_controller.update_product_details(
                    product_id=product_data['id'], active=product_data['activo'], **form_data
                )
            
            if success:
                CTkMessagebox(title="Éxito", message=message, icon="check")
                self._load_products()
                dialog.destroy()
            else:
                message_label.configure(text=message)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Guardar", command=on_submit).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=dialog.destroy).pack(side="left", padx=10)

    def _go_back_to_admin_panel(self):
        self.master.show_admin_panel_frame(self.user_info)