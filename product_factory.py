from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier

class ProductFactory:
    """Factory class for creating products."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, **kwargs) -> Product:
        """
        Create a product based on the type.

        Args:
            product_type: Type of product ("physical" or "digital")
            product_id: Unique identifier for the product
            name: Product name
            price: Product price
            stock_quantity: Initial stock quantity
            supplier: Supplier object
            **kwargs: Additional arguments (weight for physical, download_size for digital)

        Returns:
            Product: The created product instance

        Raises:
            ValueError: If product_type is unknown
        """
        if product_type == "physical":
            weight = kwargs.get("weight", 0.0)
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif product_type == "digital":
            download_size = kwargs.get("download_size", 0.0)
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
