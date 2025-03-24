# Simple E-commerce Inventory Management

A Python-based inventory management system with a GUI for a small e-commerce store.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`
3. Run tests: `pytest tests.py -v`

## Features
- Add, remove, update product quantities, and update prices via a PyQt6 GUI.
- Input fields clear after successful add, update quantity, or update price actions.
- View all products in a table format.
- Categories: Electronics and Books (hardcoded for simplicity).

## Project Structure
- `inventory.py`: Core logic (Category, Product, ProductFactory, Inventory).
- `main.py`: GUI implementation using PyQt6.
- `tests.py`: Unit tests for core logic.

## Design Decisions
- **OOP**: Separated core logic and GUI for modularity.
- **Design Pattern**: Factory pattern via `ProductFactory` for product creation.
- **GUI**: Built with PyQt6 for a modern, flexible interface with a table for product display.
- **Error Handling**: Explicit validation in GUI layer; Core logic uses `ValueError` for invalid states.
