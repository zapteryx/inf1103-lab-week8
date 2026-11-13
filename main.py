import json
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier
from file_utils import get_positive_float

def load_inventory(suppliers: list[Supplier]):
    inventory = Inventory()
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
            print("inventory.json found.")
            inventory.load_products(data["products"], suppliers)
    except FileNotFoundError:
        print("inventory.json not found. Using blank inventory.")
    return inventory

def save_inventory(inventory: Inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory.to_dict(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")

def load_suppliers():
    suppliers: list[Supplier] = []
    try:
        with open("suppliers.json", "r") as file:
            data = json.load(file)
            print("suppliers.json found.")
            for supplier_data in data["suppliers"]:
                supplier = Supplier(
                    supplier_data["supplier_id"],
                    supplier_data["name"],
                    supplier_data["contact_email"],
                )
                suppliers.append(supplier)
    except FileNotFoundError:
        print("suppliers.json not found. Using blank supplier list.")
    return suppliers

def save_suppliers(suppliers: list[Supplier]):
    suppliers_list: list[dict[str, str | float | int]] = []
    for supplier in suppliers:
        suppliers_list.append({
            "supplier_id": supplier.supplier_id,
            "name": supplier.name,
            "contact_email": supplier.contact_email,
        })
    with open("suppliers.json", "w") as file:
        suppliers_data = {"suppliers": suppliers_list}
        json.dump(suppliers_data, file, indent=4)
    print("Suppliers saved successfully to suppliers.json.")

def get_menu_option():
    print()
    print("-" * 10, "MENU", "-" * 10)
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory and Suppliers")
    print("6. Add Supplier")
    print("7. Create Order")
    print("8. Exit")
    print("-" * 26)
    print()
    while True:
        option = input("Enter option: ")
        try:
            option = int(option)
            if 1 <= option <= 8:
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please try again.")
    return option

def add_product_wizard(inventory: Inventory, suppliers: list[Supplier]):
    print("Add New Product")
    while True:
        product_type = input("Product Type (Physical / Digital): ")
        if str.lower(product_type) not in ["physical", "digital"]:
            print("Product Type can only be Physical or Digital.")
            continue
        break
    while True:
        product_id = input("Product ID: ")
        if inventory.find_product(product_id) is not None:
            print(
                "Product ID already exists. Please use a different Product ID."
            )
            continue
        break
    while True:
        product_name = input("Product Name: ")
        if product_name == "":
            print("Please provide a Product Name.")
            continue
        break
    product_price = get_positive_float("Price: ")
    while True:
        product_stock = input("Stock Quantity: ")
        try:
            product_stock = int(product_stock)
            if product_stock < 0:
                print("The entered Stock Quantity cannot be negative.")
                continue
        except ValueError:
            print("The entered Stock Quantity is not a valid number.")
            continue
        break
    while True:
        supplier_id = input("Supplier ID: ")
        supplier = None
        for s in suppliers:
            if s.supplier_id == supplier_id:
                supplier = s
                break
        if supplier is None:
            print(
                "Could not find a supplier with that Supplier ID. Please add the supplier first."
            )
            return
        break
    product_weight = 0
    product_download_size = 0
    if product_type == "physical":
        product_weight = get_positive_float("Product Weight (kg): ")
    elif product_type == "digital":
        product_download_size = get_positive_float("Product Download Size (MB): ")
    print()
    if product_type == "physical":
        product = ProductFactory.create(
            "physical",
            product_id,
            product_name,
            product_price,
            product_stock,
            supplier,
            weight=product_weight
        )
    elif product_type == "digital":
        product = ProductFactory.create(
            "digital",
            product_id,
            product_name,
            product_price,
            product_stock,
            supplier,
            download_size=product_download_size
        )
    else:
        raise ValueError("Invalid product type.")
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock_wizard(inventory: Inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")
    product = inventory.find_product(product_id)
    if product is None:
        print("Could not find a product with that Product ID. Returning to menu.")
        return
    print("Product Found:")
    product.display_information()
    print()
    while True:
        try:
            new_stock_qty = input("New Stock Quantity: ")
            new_stock_qty = int(new_stock_qty)
            if new_stock_qty < 0:
                print(
                    "The entered Stock Quantity cannot be negative. Please try again."
                )
        except ValueError:
            print(
                "The entered Stock Quantity is not a valid number. Please try again."
            )
            continue
        break
    product.update_stock(new_stock_qty)
    print()
    print("Stock updated successfully!")

def find_product_wizard(inventory: Inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    product = inventory.find_product(product_id)
    if product is None:
        print("Could not find a product with that Product ID. Returning to menu.")
        return
    print("Product Found")
    print("-" * 50)
    product.display_information()
    print("-" * 50)

def add_supplier_wizard(suppliers: list[Supplier]):
    print("Add New Supplier")
    while True:
        supplier_id = input("Supplier ID: ")
        if supplier_id == "":
            print("Please provide a Supplier ID.")
            continue
        break
    while True:
        supplier_name = input("Supplier Name: ")
        if supplier_name == "":
            print("Please provide a Supplier Name.")
            continue
        break
    while True:
        supplier_email = input("Supplier Contact Email: ")
        if supplier_email == "":
            print("Please provide a Supplier Contact Email.")
            continue
        break
    supplier = Supplier(supplier_id, supplier_name, supplier_email)
    print()
    print("Supplier added successfully!")
    suppliers.append(supplier)

def create_order_wizard(inventory: Inventory):
    print("Create New Order")
    while True:
        order_id = input("Order ID: ")
        if order_id == "":
            print("Please provide an Order ID.")
            continue
        break

    order = Order(order_id)
    while True:
        action = input("Enter 'add' to add product, 'remove' to remove product line, or 'done' to finish: ").lower()
        if action == "done":
            break
        elif action == "remove":
            prod_id_to_remove = input("Enter Product ID of line to remove: ")
            if order.remove_order_line(prod_id_to_remove):
                print(f"Removed line with Product ID {prod_id_to_remove} from order.")
            else:
                print("No line found matching that Product ID in current order.")
            continue
        elif action != "add":
            print("Invalid action. Please enter 'add', 'remove', or 'done'.")
            continue

        product_id = input("Enter Product ID: ")
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found in inventory. Please try again.")
            continue

        while True:
            quantity_input = input("Enter Quantity: ")
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")

        order.add_order_line(product, quantity)
        print(f"Added {quantity} x {product.name} to order.")

    if not order.order_lines:
        print("No items added to the order.")
        return

    print()
    order.display_order_summary()

def main():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print()
    suppliers = load_suppliers()
    print("Suppliers loaded successfully.")
    inventory = load_inventory(suppliers)
    print("Inventory loaded successfully.")
    while True:
        option = get_menu_option()
        print()
        if option == 1:
            inventory.display_all()
        elif option == 2:
            add_product_wizard(inventory, suppliers)
        elif option == 3:
            update_stock_wizard(inventory)
        elif option == 4:
            find_product_wizard(inventory)
        elif option == 5:
            print("Saving inventory and suppliers...")
            save_inventory(inventory)
            save_suppliers(suppliers)
        elif option == 6:
            add_supplier_wizard(suppliers)
        elif option == 7:
            create_order_wizard(inventory)
        elif option == 8:
            print("Saving inventory and suppliers before exit...")
            save_inventory(inventory)
            save_suppliers(suppliers)
            print()
            print("Thank you for using Inventory Management System.")
            exit()


if __name__ == "__main__":
    main()