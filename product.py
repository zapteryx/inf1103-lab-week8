class Product:
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
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self._weight:.2f}kg")

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self._download_size:.2f} MB")
