class Product:
    def __init__(self, product_id, name, price, stock):
        self._id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

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