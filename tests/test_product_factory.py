import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from product_factory import ProductFactory
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    """Test ProductFactory creation methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_create_physical_product(self):
        """Test factory creates PhysicalProduct correctly."""
        product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.0, 10,
            self.supplier, weight=2.5
        )
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.id, "P001")
        self.assertEqual(product.name, "Desk Lamp")
        self.assertEqual(product.price, 25.0)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.weight, 2.5)

    def test_create_digital_product(self):
        """Test factory creates DigitalProduct correctly."""
        product = ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100,
            self.supplier, download_size=150.5
        )
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.id, "D001")
        self.assertEqual(product.name, "Photo Editor")
        self.assertEqual(product.price, 49.90)
        self.assertEqual(product.stock, 100)
        self.assertEqual(product.download_size, 150.5)

    def test_create_unknown_product_type(self):
        """Test factory raises ValueError for unknown product type."""
        with self.assertRaises(ValueError) as context:
            ProductFactory.create(
                "service", "S001", "Installation", 30.0, 5, self.supplier
            )
        self.assertIn("Unknown product type", str(context.exception))

    def test_factory_returns_product_type(self):
        """Test factory returns base Product type."""
        product = ProductFactory.create(
            "physical", "P001", "Test", 10.0, 5,
            self.supplier, weight=1.0
        )
        self.assertIsInstance(product, Product)


if __name__ == '__main__':
    unittest.main()
