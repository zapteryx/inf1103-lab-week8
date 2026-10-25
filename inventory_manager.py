import json

def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
            print("inventory.json found.")
            return data
    except FileNotFoundError:
        print("inventory.json not found. Using blank inventory.")
        return {"products": []}

def get_menu_option():
    print()
    print("-" * 10, "MENU", "-" * 10)
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 26)
    print()
    while True:
        option = input("Enter option: ")
        try:
            option = int(option)
            if option >= 1 and option <= 6:
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please try again.")
    return option

def display_products(inventory):
    print("Current Inventory")
    print("-" * 50)
    if len(inventory["products"]) == 0:
        print("There are no items in the inventory.")
    else:
        for product in inventory["products"]:
            print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 50)

def search_for_product(inventory, id):
    for product in inventory["products"]:
        if product["id"] == id:
            return product
    return None

def add_product_wizard(inventory):
    print("Add New Product")
    product = {}
    while True:
        product["id"] = input("Product ID: ")
        if search_for_product(inventory, product["id"]) != None:
            print("Product ID already exists. Please use a different Product ID.")
            continue
        break
    while True:
        product["name"] = input("Product Name: ")
        if product["name"] == "":
            print("Please provide a Product Name.")
            continue
        break
    while True:
        product["price"] = input("Price: ")
        try:
            product["price"] = float(product["price"])
            if product["price"] < 0:
                print("The entered Price cannot be negative.")
                continue
        except ValueError:
            print("The entered Price is not a valid number.")
            continue
        break
    while True:
        product["stock"] = input("Stock Quantity: ")
        try:
            product["stock"] = int(product["stock"])
            if product["stock"] < 0:
                print("The entered Stock Quantity cannot be negative.")
                continue
        except ValueError:
            print("The entered Stock Quantity is not a valid number.")
            continue
        break
    print()
    inventory["products"].append(product)
    print("Product added successfully!")

def update_stock_wizard(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")
    product = search_for_product(inventory, product_id)
    if product == None:
        print("Could not find a product with that Product ID. Returning to menu.")
        return
    print("Product Found:")
    print("Name:", product["name"])
    print("Current Stock:", product["stock"])
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
    product["stock"] = new_stock_qty
    print()
    print("Stock updated successfully!")

def search_product_wizard(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    product = search_for_product(inventory, product_id)
    if product == None:
        print("Could not find a product with that Product ID. Returning to menu.")
        return
    print("Product Found")
    print("-" * 50)
    print("ID:", product["id"])
    print("Name:", product["name"])
    print(f"Price: ${product["price"]:.2f}")
    print("Stock:", product["stock"])
    print("-" * 50)

def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully to inventory.json.")

print("=" * 50)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 50)
print()
inventory = load_inventory()
print("Inventory loaded successfully.")
while True:
    option = get_menu_option()
    print()
    if option == 1:
        display_products(inventory)
    elif option == 2:
        add_product_wizard(inventory)
    elif option == 3:
        update_stock_wizard(inventory)
    elif option == 4:
        search_product_wizard(inventory)
    elif option == 5:
        print("Saving inventory...")
        save_inventory(inventory)
    elif option == 6:
        print("Saving inventory before exit...")
        save_inventory(inventory)
        print()
        print("Thank you for using Inventory Management System.")
        exit()