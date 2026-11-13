import csv
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

def get_positive_float(prompt: str) -> float:
    """
    Prompt user for a positive float and keep asking until valid input is provided.

    Args:
        prompt: The prompt message to display

    Returns:
        float: A valid positive float value
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """
    Load products from a CSV file into the inventory.

    Args:
        path: Path to the CSV file
        inventory: Inventory instance to add products to
        supplier: Supplier to associate with products
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header row
            loaded = 0

            for row in reader:
                try:
                    if len(row) < 4:
                        print(f"Skipping invalid row (not enough columns): {row}")
                        continue

                    product_type = row[0]
                    product_id = row[1]
                    name = row[2]
                    price = float(row[3])
                    stock_quantity = int(row[4]) if len(row) > 4 else 0

                    # Create product through factory
                    if product_type == "physical":
                        weight = float(row[5]) if len(row) > 5 else 1.0
                        product = ProductFactory.create(product_type, product_id, name,
                                                       price, stock_quantity, supplier,
                                                       weight=weight)
                    elif product_type == "digital":
                        download_size = float(row[5]) if len(row) > 5 else 1.0
                        product = ProductFactory.create(product_type, product_id, name,
                                                       price, stock_quantity, supplier,
                                                       download_size=download_size)
                    else:
                        raise ValueError(f"Unknown product type: {product_type}")

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as e:
                    print(f"Skipping invalid row: {row} - {e}")
                    continue

            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
