from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self._id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def id(self):
        return self._id

    def display_information(self):
        print(f"ID: {self._id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def update_stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = new_stock

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self._weight:.2f}kg")

    def get_fulfilment_info(self):
        print("The product requires shipping.")

    def calculate_shipping_cost(self):
        return 1.5 * self._weight

    def to_dict(self):
        product = super().to_dict()
        product["type"] = "physical"
        product["weight"] = self._weight
        return product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")

    def get_fulfilment_info(self):
        print("The product will be delivered digitally.")

    def to_dict(self):
        product = super().to_dict()
        product["type"] = "digital"
        product["download_size"] = self._download_size
        return product
