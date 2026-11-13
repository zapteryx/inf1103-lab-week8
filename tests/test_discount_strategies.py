import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discount_strategy import (
    DiscountStrategy, NoDiscount, PercentageDiscount,
    BulkDiscount, StudentDiscount
)
from order import Order
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier
from order_line import OrderLine


class TestDiscountStrategies(unittest.TestCase):
    """Test discount strategy implementations."""

    def test_no_discount(self):
        """Test NoDiscount returns total unchanged."""
        discount = NoDiscount()
        self.assertEqual(discount.apply(100.0), 100.0)
        self.assertEqual(discount.apply(250.0), 250.0)

    def test_percentage_discount(self):
        """Test PercentageDiscount applies correct percentage."""
        discount = PercentageDiscount(10)
        self.assertEqual(discount.apply(100.0), 90.0)
        self.assertEqual(discount.apply(250.0), 225.0)

        discount = PercentageDiscount(5)
        self.assertEqual(discount.apply(100.0), 95.0)

    def test_bulk_discount(self):
        """Test BulkDiscount applies when threshold is met."""
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(250.0), 230.0)
        self.assertEqual(discount.apply(200.0), 180.0)
        self.assertEqual(discount.apply(150.0), 150.0)  # Below threshold

    def test_student_discount(self):
        """Test StudentDiscount applies 5% discount."""
        discount = StudentDiscount()
        self.assertEqual(discount.apply(100.0), 95.0)
        self.assertEqual(discount.apply(200.0), 190.0)


class TestOrderWithDiscount(unittest.TestCase):
    """Test Order class with discount strategies."""

    def setUp(self):
        """Set up test fixtures."""
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.product1 = PhysicalProduct("P001", "Product 1", 50.0, 10, self.supplier, 1.0)
        self.product2 = PhysicalProduct("P002", "Product 2", 100.0, 5, self.supplier, 2.0)

    def test_order_with_no_discount(self):
        """Test order total with no discount."""
        order = Order("O001")
        order.add_order_line(self.product1, 2)  # 100
        order.add_order_line(self.product2, 1)  # 100
        self.assertEqual(order.calculate_total(), 200.0)

    def test_order_with_percentage_discount(self):
        """Test order total with percentage discount."""
        order = Order("O001", PercentageDiscount(10))
        order.add_order_line(self.product1, 2)  # 100
        order.add_order_line(self.product2, 1)  # 100
        # Total = 200, with 10% discount = 180
        self.assertEqual(order.calculate_total(), 180.0)

    def test_order_with_bulk_discount(self):
        """Test order total with bulk discount."""
        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(self.product1, 3)  # 150
        order.add_order_line(self.product2, 1)  # 100
        # Total = 250, meets threshold, discount 20 = 230
        self.assertEqual(order.calculate_total(), 230.0)

    def test_change_discount_strategy(self):
        """Test changing discount strategy on existing order."""
        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(self.product1, 3)  # 150
        order.add_order_line(self.product2, 1)  # 100
        # Total = 250 with bulk discount
        self.assertEqual(order.calculate_total(), 230.0)

        # Change to percentage discount
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

        # Change to no discount
        order.set_discount(NoDiscount())
        self.assertEqual(order.calculate_total(), 250.0)


if __name__ == '__main__':
    unittest.main()
