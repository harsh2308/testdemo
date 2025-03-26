# Simple E-commerce Inventory Management

A Python-based inventory management system with a GUI and CLI for a small e-commerce store.

## Quick Setup
1. Clone the repository:
    ```
    git clone https://github.com/harsh2308/testdemo.git
    cd testdemo
    ```

2. Install dependencies
    ```
    pip install -r requirements.txt
    ```

3. Run the GUI application:
    ```
    python demo/main.py
    ```

## Test the Application
1. Run the unit tests:
    ```
    pytest tests/test_inventory.py -v
    ```

## CLI Commands
Test the inventory system quickly using the CLI:
1. Run CLI Commands:
    ```
    python commands.py
    ```
2. Once the script is running, use the following commands:
    add – Add a new product to the inventory.
    list – List all products in the inventory.
    exit – Exit the application.

    ## Example
    ```
    > add
    Enter SKU: 12345
    Enter Name: Laptop
    Enter Price: 999.99
    Enter Quantity: 5
    Enter Category (Electronics/Books): Electronics
    Product added: Laptop (SKU: 12345) - $999.99 - Quantity: 5

    > list
    Laptop (SKU: 12345) - $999.99 - Quantity: 5

    > exit
    Exiting...
    ```
