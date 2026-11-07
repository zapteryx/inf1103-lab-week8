from abc import ABC, abstractmethod
from supplier import Supplier

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self._id: str = product_id
        self._name: str = name
        self._price: float = price
        self._stock: int = stock
        self._supplier: Supplier = supplier

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    @property
    def supplier(self):
        return self._supplier

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    def display_information(self):
        print(f"ID: {self._id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def update_stock(self, new_stock: int):
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock: int = new_stock

    def to_dict(self) -> dict[str, str | float | int]:
        return {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "supplier": self._supplier.supplier_id
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = weight

    @property
    def type(self):
        return "physical"

    @property
    def weight(self):
        return self._weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self._weight:.2f}kg")

    def get_fulfilment_info(self):
        return f"The product requires shipping. Shipping cost: ${self.calculate_shipping_cost():.2f}"

    def calculate_shipping_cost(self):
        return 1.5 * self._weight

    def to_dict(self) -> dict[str, str | float | int]:
        product: dict[str, str | float | int] = super().to_dict()
        product["type"] = "physical"
        product["weight"] = self._weight
        return product

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = download_size

    @property
    def type(self):
        return "digital"

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")

    def get_fulfilment_info(self):
        return "The product will be delivered digitally."

    def to_dict(self) -> dict[str, str | float | int]:
        product: dict[str, str | float | int] = super().to_dict()
        product["type"] = "digital"
        product["download_size"] = self._download_size
        return product
