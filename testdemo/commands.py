from demo.models.inventory import Inventory, ProductFactory, Category

def initialize_inventory():
    return Inventory(), {
        "Electronics": Category("Electronics", "Devices"),
        "Books": Category("Books", "Literature")
    }

def display_menu():
    print("\nSimple Inventory CLI")
    print("Commands: add, list, exit")

def handle_add_product(inventory, categories):
    sku = input("Enter SKU: ")
    name = input("Enter Name: ")
    try:
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
    except ValueError:
        print("Error: Price must be a number and quantity an integer.")
        return
    
    category_name = input("Enter Category (Electronics/Books): ")
    category = categories.get(category_name)
    if not category:
        print("Error: Invalid category. Use 'Electronics' or 'Books'.")
        return
    
    try:
        product = ProductFactory.create_product(sku, name, price, category, quantity)
        inventory.add_product(product)
        print(f"Product added: {product}")
    except ValueError as e:
        print(f"Error: {e}")

def handle_list_products(inventory):
    products = inventory.get_all_products()
    if not products:
        print("No products in inventory.")
    else:
        for product in products:
            print(product)

def main():
    inventory, categories = initialize_inventory()
    display_menu()
    
    while True:
        command = input("> ").strip().lower()
        if command == "exit":
            print("Exiting...")
            break
        elif command == "add":
            handle_add_product(inventory, categories)
        elif command == "list":
            handle_list_products(inventory)
        else:
            print("Unknown command. Use: add, list, exit")

if __name__ == "__main__":
    main()
