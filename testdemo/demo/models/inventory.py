from typing import List, Optional

class Category:
    """
    Represents a product category.
    """
    def __init__(self, name: str, description: str):
        """
        Initialize a Category with a name and description.
        
        Args:
            name (str): The name of the category.
            description (str): A brief description of the category.
        """
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """
        Return a string representation of the category.
        """
        return f"{self.name}: {self.description}"

    def get_details(self) -> dict:
        """
        Retrieve the category's details as a dictionary.
        """
        return {"name": self.name, "description": self.description}


class Product:
    """
    Represents a product in the inventory.
    """
    def __init__(self, sku: str, name: str, price: float, category: Category, quantity: int):
        if not sku or not name or price < 0 or quantity < 0:
            raise ValueError("Invalid product data")
        self.sku = sku
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name} (SKU: {self.sku}) - ${self.price}, Qty: {self.quantity}"

    def get_details(self) -> dict:
        """
        Retrieve product details.
        """
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "category": str(self.category),
            "quantity": self.quantity
        }

    def update_price(self, new_price: float) -> None:
        """
        Update product price.
        """
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def update_quantity(self, new_quantity: int) -> None:
        """
        Update product quantity.
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity


class ProductFactory:
    """
    Factory class to create Product instances.
    Design Pattern Choice: Factory - Centralizes product creation logic and ensures
    valid objects are instantiated with proper validation. This pattern is chosen because
    it encapsulates the object creation process, making it easier to enforce constraints
    (e.g., valid SKU, price, quantity) and allows for future extensibility (e.g., creating
    different types of products) without modifying the core Product class.
    """
    @staticmethod
    def create_product(sku: str, name: str, price: float, category: Category, quantity: int) -> Product:
        """
        Create a new Product instance with validation.
        """
        return Product(sku, name, price, category, quantity)


class Inventory:
    """
    Manages the collection of products.
    """
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product) -> None:
        """
        Add a product to the inventory.
        """
        if product.sku in self.products:
            raise ValueError(f"Product with SKU {product.sku} already exists")
        self.products[product.sku] = product

    def remove_product(self, sku: str) -> None:
        """
        Remove a product by SKU.
        """
        if sku not in self.products:
            raise ValueError(f"Product with SKU {sku} not found")
        del self.products[sku]

    def get_product(self, sku: str) -> Optional[Product]:
        """
        Retrieve a product by SKU.
        """
        if sku not in self.products:
            raise ValueError(f"Product with SKU {sku} not found")
        return self.products[sku]

    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products in the inventory.
        """
        return list(self.products.values())

    def get_products_by_category(self, category: Category) -> List[Product]:
        """
        Retrieve all products within a specific category.
        """
        return [p for p in self.products.values() if p.category == category]
