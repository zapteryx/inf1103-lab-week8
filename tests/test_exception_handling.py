import unittest
import sys
import os
import tempfile
import csv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_utils import load_products
from inventory import Inventory
from supplier import Supplier


class TestFileLoading(unittest.TestCase):
    """Test exception handling for file loading."""

    def setUp(self):
        """Set up test fixtures."""
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.inventory = Inventory()

    def test_load_missing_file(self):
        """Test that missing file is handled gracefully."""
        # Should not raise exception, just print message
        load_products("nonexistent_file.csv", self.inventory, self.supplier)
        # If we get here without exception, test passes
        self.assertEqual(len(self.inventory._products), 0)

    def test_load_valid_products(self):
        """Test loading valid products from CSV."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            writer.writerow(['product_type', 'product_id', 'name', 'price', 'stock_quantity'])
            writer.writerow(['physical', 'P001', 'Desk Lamp', '25.00', '10'])
            writer.writerow(['digital', 'D001', 'Photo Editor', '49.90', '100'])
            temp_path = f.name

        try:
            load_products(temp_path, self.inventory, self.supplier)
            self.assertEqual(len(self.inventory._products), 2)
        finally:
            os.unlink(temp_path)

    def test_load_skips_invalid_rows(self):
        """Test that invalid rows are skipped and valid ones loaded."""
        # Create temporary CSV file with mix of valid and invalid rows
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            writer.writerow(['product_type', 'product_id', 'name', 'price', 'stock_quantity'])
            writer.writerow(['physical', 'P001', 'Desk Lamp', '25.00', '10'])
            writer.writerow(['service', 'S001', 'Installation', '30.00', '5'])  # Invalid type
            writer.writerow(['physical', 'P002', 'Chair', 'abc', '3'])  # Invalid price
            writer.writerow(['physical', 'P003', 'Monitor Stand', '39.50', '7'])
            temp_path = f.name

        try:
            load_products(temp_path, self.inventory, self.supplier)
            # Should load 2 valid products, skip 2 invalid ones
            self.assertEqual(len(self.inventory._products), 2)
            self.assertIsNotNone(self.inventory.find_product('P001'))
            self.assertIsNotNone(self.inventory.find_product('P003'))
            self.assertIsNone(self.inventory.find_product('S001'))
            self.assertIsNone(self.inventory.find_product('P002'))
        finally:
            os.unlink(temp_path)

    def test_load_handles_invalid_price(self):
        """Test that invalid price values are caught and row skipped."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            writer.writerow(['product_type', 'product_id', 'name', 'price', 'stock_quantity'])
            writer.writerow(['physical', 'P001', 'Test', 'not_a_number', '10'])
            temp_path = f.name

        try:
            load_products(temp_path, self.inventory, self.supplier)
            self.assertEqual(len(self.inventory._products), 0)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
