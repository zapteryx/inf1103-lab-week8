"""
Demo script showcasing Lab 9 features:
- Strategy pattern for discounts
- Factory pattern for product creation
- Validation
- Exception handling
"""

from supplier import Supplier
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from file_utils import load_products

def demo_strategy_pattern():
    """Demonstrate different discount strategies."""
    print("=" * 50)
    print("STRATEGY PATTERN DEMO - Order Discounts")
    print("=" * 50)

    # Create test supplier and products
    supplier = Supplier("S001", "Demo Supplier", "demo@example.com")
    product1 = ProductFactory.create("physical", "P001", "Desk Lamp", 50.0, 10, supplier, weight=2.0)
    product2 = ProductFactory.create("digital", "D001", "Software", 100.0, 50, supplier, download_size=150.0)

    # Create order
    order = Order("O001")
    order.add_order_line(product1, 3)  # 150
    order.add_order_line(product2, 1)  # 100
    # Total: 250

    print(f"\nOrder Items: 3x {product1.name} + 1x {product2.name}")
    print(f"Subtotal: $250.00")

    # No discount
    print(f"\n1. No Discount: ${order.calculate_total():.2f}")

    # Percentage discount
    order.set_discount(PercentageDiscount(10))
    print(f"2. 10% Discount: ${order.calculate_total():.2f}")

    # Bulk discount
    order.set_discount(BulkDiscount(200, 20))
    print(f"3. Bulk Discount ($20 off $200+): ${order.calculate_total():.2f}")

    # Student discount
    order.set_discount(StudentDiscount())
    print(f"4. Student Discount (5%): ${order.calculate_total():.2f}")

def demo_factory_pattern():
    """Demonstrate product creation through factory."""
    print("\n" + "=" * 50)
    print("FACTORY PATTERN DEMO - Product Creation")
    print("=" * 50)

    supplier = Supplier("S002", "Factory Demo Supplier", "factory@example.com")

    # Create products through factory
    physical = ProductFactory.create("physical", "P100", "Office Chair", 199.99, 5, supplier, weight=15.0)
    digital = ProductFactory.create("digital", "D100", "Cloud Storage", 9.99, 1000, supplier, download_size=0.1)

    print(f"\nCreated Physical Product: {physical.name} - ${physical.price:.2f}")
    print(f"Created Digital Product: {digital.name} - ${digital.price:.2f}")

    # Try creating invalid product type
    try:
        invalid = ProductFactory.create("service", "S100", "Consulting", 150.0, 1, supplier)
    except ValueError as e:
        print(f"\nFactory caught invalid type: {e}")

def demo_validation():
    """Demonstrate validation rules."""
    print("\n" + "=" * 50)
    print("VALIDATION DEMO")
    print("=" * 50)

    supplier = Supplier("S003", "Validation Supplier", "validation@example.com")

    # Invalid price
    try:
        ProductFactory.create("physical", "P200", "Invalid", -10.0, 5, supplier, weight=1.0)
    except ValueError as e:
        print(f"\n✓ Caught invalid price: {e}")

    # Invalid stock
    try:
        ProductFactory.create("physical", "P201", "Invalid", 10.0, -5, supplier, weight=1.0)
    except ValueError as e:
        print(f"✓ Caught invalid stock: {e}")

    # Invalid order quantity
    valid_product = ProductFactory.create("physical", "P202", "Valid", 10.0, 5, supplier, weight=1.0)
    order = Order("O100")
    try:
        order.add_order_line(valid_product, 0)
    except ValueError as e:
        print(f"✓ Caught invalid quantity: {e}")

def demo_exception_handling():
    """Demonstrate exception handling for file loading."""
    print("\n" + "=" * 50)
    print("EXCEPTION HANDLING DEMO - File Loading")
    print("=" * 50)

    supplier = Supplier("S004", "File Supplier", "file@example.com")
    inventory = Inventory()

    print("\n1. Loading from existing file (products.csv):")
    load_products("products.csv", inventory, supplier)
    print(f"   Products in inventory: {len(inventory._products)}")

    print("\n2. Loading from non-existent file:")
    inventory2 = Inventory()
    load_products("does_not_exist.csv", inventory2, supplier)
    print(f"   Products in inventory: {len(inventory2._products)}")

if __name__ == "__main__":
    demo_strategy_pattern()
    demo_factory_pattern()
    demo_validation()
    demo_exception_handling()

    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("=" * 50)
