import pytest
from demo.models.inventory import Category, Product, ProductFactory, Inventory

def test_category_creation():
    cat = Category("Books", "Printed literature")
    assert cat.name == "Books"
    assert cat.description == "Printed literature"
    assert str(cat) == "Books: Printed literature"
    assert cat.get_details() == {"name": "Books", "description": "Printed literature"}

def test_product_creation():
    cat = Category("Books", "Printed literature")
    prod = ProductFactory.create_product("SKU001", "Python Book", 29.99, cat, 5)
    assert prod.sku == "SKU001"
    assert prod.name == "Python Book"
    assert prod.price == 29.99
    assert prod.quantity == 5
    assert str(prod) == "Python Book (SKU: SKU001) - $29.99, Qty: 5"

def test_product_invalid_input():
    cat = Category("Books", "Printed literature")
    with pytest.raises(ValueError):
        ProductFactory.create_product("", "Book", -1, cat, -5)

def test_inventory_add_product():
    cat = Category("Books", "Printed literature")
    prod = ProductFactory.create_product("SKU001", "Python Book", 29.99, cat, 5)
    inv = Inventory()
    inv.add_product(prod)
    assert inv.get_product("SKU001") == prod

def test_inventory_duplicate_product():
    cat = Category("Books", "Printed literature")
    prod = ProductFactory.create_product("SKU001", "Python Book", 29.99, cat, 5)
    inv = Inventory()
    inv.add_product(prod)
    with pytest.raises(ValueError):
        inv.add_product(prod)

def test_inventory_remove_product():
    cat = Category("Books", "Printed literature")
    prod = ProductFactory.create_product("SKU001", "Python Book", 29.99, cat, 5)
    inv = Inventory()
    inv.add_product(prod)
    inv.remove_product("SKU001")
    with pytest.raises(ValueError):
        inv.get_product("SKU001")

def test_inventory_get_products_by_category():
    cat1 = Category("Books", "Printed literature")
    cat2 = Category("Electronics", "Devices")
    prod1 = ProductFactory.create_product("SKU001", "Python Book", 29.99, cat1, 5)
    prod2 = ProductFactory.create_product("SKU002", "Laptop", 999.99, cat2, 2)
    inv = Inventory()
    inv.add_product(prod1)
    inv.add_product(prod2)
    books = inv.get_products_by_category(cat1)
    assert len(books) == 1
    assert books[0].sku == "SKU001"
