class Inventory:
    def __init__(self):
        self._products = []

    def search_product(self, product_id):
        for p in self._products:
            if p.id == product_id:
                return p
        return None

    def add_product(self, product):
        p = self.search_product(product.id)
        if p is not None:
            raise ValueError("Product ID already exists.")
        self._products.append(product)

    def display_all(self):
        print("Current Inventory")
        print("-" * 50)
        if not self._products:
            print("There are no items in the inventory.")
            return
        for product in self._products:
            print(f"ID: {product.id} | Name: {product.name} | Price: ${product.price:.2f} | Stock: {product.stock}")
        print("-" * 50)

    def to_dict(self):
        products = []
        for product in self._products:
            products.append(product.to_dict())
        return {"products": products}