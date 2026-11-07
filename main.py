import json
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier

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
                    supplier_data["contact_email"]
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
            "contact_email": supplier.contact_email
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
    print("7. Exit")
    print("-" * 26)
    print()
    while True:
        option = input("Enter option: ")
        try:
            option = int(option)
            if option >= 1 and option <= 7:
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
            print("Product ID already exists. Please use a different Product ID.")
            continue
        break
    while True:
        product_name = input("Product Name: ")
        if product_name == "":
            print("Please provide a Product Name.")
            continue
        break
    while True:
        product_price = input("Price: ")
        try:
            product_price = float(product_price)
            if product_price < 0:
                print("The entered Price cannot be negative.")
                continue
        except ValueError:
            print("The entered Price is not a valid number.")
            continue
        break
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
            print("Could not find a supplier with that Supplier ID. Please add the supplier first.")
            return
        break
    product_weight = 0
    product_download_size = 0
    if product_type == "physical":
        while True:
            product_weight = input("Product Weight (kg): ")
            try:
                product_weight = float(product_weight)
                if product_weight < 0:
                    print("The entered Weight cannot be negative.")
                    continue
            except ValueError:
                print("The entered Weight is not a valid number.")
                continue
            break
    elif product_type == "digital":
        while True:
            product_download_size = input("Product Download Size (MB): ")
            try:
                product_download_size = float(product_download_size)
                if product_download_size < 0:
                    print("The entered Download Size cannot be negative.")
                    continue
            except ValueError:
                print("The entered Download Size is not a valid number.")
                continue
            break
    print()
    if product_type == "physical":
        product = PhysicalProduct(product_id, product_name, product_price, product_stock, supplier, product_weight)
    elif product_type == "digital":
        product = DigitalProduct(product_id, product_name, product_price, product_stock, supplier, product_download_size)
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
                print("The entered Stock Quantity cannot be negative. Please try again.")
        except ValueError:
            print("The entered Stock Quantity is not a valid number. Please try again.")
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
            print("Saving inventory and suppliers before exit...")
            save_inventory(inventory)
            save_suppliers(suppliers)
            print()
            print("Thank you for using Inventory Management System.")
            exit()

if __name__ == "__main__":
    main()