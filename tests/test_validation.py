import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier
from order_line import OrderLine


class TestValidation(unittest.TestCase):
    """Test validation rules for products and order lines."""

    def setUp(self):
        """Set up test fixtures."""
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_product_price_must_be_positive(self):
        """Test that product price must be greater than zero."""
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P001", "Test", 0.0, 10, self.supplier, 1.0)
        self.assertIn("Price must be greater than zero", str(context.exception))

        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Test", -5.0, 10, self.supplier, 1.0)

    def test_product_stock_cannot_be_negative(self):
        """Test that product stock cannot be negative."""
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P001", "Test", 10.0, -1, self.supplier, 1.0)
        self.assertIn("Stock quantity cannot be negative", str(context.exception))

    def test_product_stock_can_be_zero(self):
        """Test that product stock can be zero (out of stock)."""
        product = PhysicalProduct("P001", "Test", 10.0, 0, self.supplier, 1.0)
        self.assertEqual(product.stock, 0)

    def test_update_stock_validates_negative(self):
        """Test that update_stock prevents negative values."""
        product = PhysicalProduct("P001", "Test", 10.0, 5, self.supplier, 1.0)
        with self.assertRaises(ValueError):
            product.update_stock(-1)

    def test_orderline_quantity_must_be_positive(self):
        """Test that OrderLine quantity must be greater than zero."""
        product = PhysicalProduct("P001", "Test", 10.0, 5, self.supplier, 1.0)

        with self.assertRaises(ValueError) as context:
            OrderLine(product, 0)
        self.assertIn("Quantity must be greater than zero", str(context.exception))

        with self.assertRaises(ValueError):
            OrderLine(product, -1)

    def test_valid_product_creation(self):
        """Test that valid products can be created."""
        product = PhysicalProduct("P001", "Test", 10.0, 5, self.supplier, 1.0)
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.stock, 5)

    def test_valid_orderline_creation(self):
        """Test that valid order lines can be created."""
        product = PhysicalProduct("P001", "Test", 10.0, 5, self.supplier, 1.0)
        line = OrderLine(product, 2)
        self.assertEqual(line.quantity, 2)
        self.assertEqual(line.calculate_subtotal(), 20.0)


if __name__ == '__main__':
    unittest.main()
