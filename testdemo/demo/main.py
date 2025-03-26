import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, 
                             QComboBox, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from models.inventory import Inventory, ProductFactory, Category

class InventoryGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inventory = Inventory()
        self.categories = [Category("Electronics", "Devices"), Category("Books", "Literature")]
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add filter section
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Category:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Categories")  # Add "All" option
        self.filter_combo.addItems([cat.name for cat in self.categories])
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Table setup
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["SKU", "Name", "Price ($)", "Category", "Quantity"])
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)
        self.refresh_table()

        # Form setup
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        self.sku_input = QLineEdit()
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.name for cat in self.categories])
        self.quantity_input = QLineEdit()

        form_layout.addWidget(QLabel("SKU:"))
        form_layout.addWidget(self.sku_input)
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Price:"))
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(QLabel("Category:"))
        form_layout.addWidget(self.category_combo)
        form_layout.addWidget(QLabel("Quantity:"))
        form_layout.addWidget(self.quantity_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Product")
        remove_button = QPushButton("Remove Product")
        update_qty_button = QPushButton("Update Quantity")
        update_price_button = QPushButton("Update Price")

        add_button.clicked.connect(self.add_product)
        remove_button.clicked.connect(self.remove_product)
        update_qty_button.clicked.connect(self.update_quantity)
        update_price_button.clicked.connect(self.update_price)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(update_qty_button)
        button_layout.addWidget(update_price_button)

        form_layout.addLayout(button_layout)
        main_layout.addWidget(form_widget)

    def refresh_table(self):
        self.table.setRowCount(0)
        current_filter = self.filter_combo.currentText()
        products = self.inventory.get_all_products()

        # Apply filter if not showing all categories
        if current_filter != "All Categories":
            products = [p for p in products if p.category.name == current_filter]

        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product.sku))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.price)))
            self.table.setItem(row, 3, QTableWidgetItem(product.category.name))
            self.table.setItem(row, 4, QTableWidgetItem(str(product.quantity)))

    def apply_filter(self):
        self.refresh_table()

    def add_product(self):
        sku = self.sku_input.text().strip()
        name = self.name_input.text().strip()
        price_str = self.price_input.text().strip()
        category_name = self.category_combo.currentText()
        quantity_str = self.quantity_input.text().strip()

        if not sku:
            QMessageBox.critical(self, "Error", "SKU cannot be empty")
            return
        if not name:
            QMessageBox.critical(self, "Error", "Name cannot be empty")
            return
        if not price_str or not price_str.replace('.', '', 1).isdigit() or float(price_str) < 0:
            QMessageBox.critical(self, "Error", "Price must be a non-negative number")
            return
        if not quantity_str or not quantity_str.isdigit() or int(quantity_str) < 0:
            QMessageBox.critical(self, "Error", "Quantity must be a non-negative integer")
            return

        price = float(price_str)
        quantity = int(quantity_str)
        category = next(cat for cat in self.categories if cat.name == category_name)

        product = ProductFactory.create_product(sku, name, price, category, quantity)
        if product.sku in [p.sku for p in self.inventory.get_all_products()]:
            QMessageBox.critical(self, "Error", f"Product with SKU {sku} already exists")
            return

        self.inventory.add_product(product)
        self.refresh_table()
        self.clear_inputs()

    def remove_product(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a product to remove")
            return

        sku = self.table.item(selected, 0).text()
        if sku not in [p.sku for p in self.inventory.get_all_products()]:
            QMessageBox.critical(self, "Error", f"Product with SKU {sku} not found")
            return

        self.inventory.remove_product(sku)
        self.refresh_table()

    def update_quantity(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a product to update")
            return

        sku = self.table.item(selected, 0).text()
        quantity_str = self.quantity_input.text().strip()

        if not quantity_str or not quantity_str.isdigit() or int(quantity_str) < 0:
            QMessageBox.critical(self, "Error", "Quantity must be a non-negative integer")
            return

        new_quantity = int(quantity_str)
        product = self.inventory.get_product(sku)
        product.update_quantity(new_quantity)
        self.refresh_table()
        self.clear_inputs()

    def update_price(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Please select a product to update")
            return

        sku = self.table.item(selected, 0).text()
        price_str = self.price_input.text().strip()

        if not price_str or not price_str.replace('.', '', 1).isdigit() or float(price_str) < 0:
            QMessageBox.critical(self, "Error", "Price must be a non-negative number")
            return

        new_price = float(price_str)
        product = self.inventory.get_product(sku)
        product.update_price(new_price)
        self.refresh_table()
        self.clear_inputs()

    def clear_inputs(self):
        self.sku_input.clear()
        self.name_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryGUI()
    window.show()
    sys.exit(app.exec())
