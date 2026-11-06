from product import Product, PhysicalProduct, DigitalProduct

class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def search_product(self, product_id: str):
        for p in self._products:
            if p.id == product_id:
                return p
        return None

    def add_product(self, product: Product):
        p: Product | None = self.search_product(product.id)
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
            product.display_information()
        print("-" * 50)

    def load_products(self, products: list[PhysicalProduct | DigitalProduct]):
        for item in products:
            if item.type == "physical" and isinstance(item, PhysicalProduct):
                self.add_product(PhysicalProduct(item.id, item.name, item.price, item.stock, item.weight))
            elif item.type == "digital" and isinstance(item, DigitalProduct):
                self.add_product(DigitalProduct(item.id, item.name, item.price, item.stock, item.download_size))

    def to_dict(self) -> dict[str, list[dict[str, str | float | int]]]:
        products: list[dict[str, str | float | int]] = []
        for product in self._products:
            products.append(product.to_dict())
        return {"products": products}