from product import Product
from product_factory import ProductFactory
from supplier import Supplier

class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def find_product(self, product_id: str):
        for p in self._products:
            if p.id == product_id:
                return p
        return None

    def add_product(self, product: Product):
        p: Product | None = self.find_product(product.id)
        if p is not None:
            raise ValueError("Product ID already exists.")
        self._products.append(product)

    def remove_product(self, product_id: str):
        p: Product | None = self.find_product(product_id)
        if p is None:
            raise ValueError("Product ID does not exist.")
        self._products.remove(p)

    def show_product_details(self, product: Product):
        product.display_information()
        print(product.get_fulfilment_info())
        product.supplier.display_information()

    def display_all(self):
        print("Current Inventory")
        print("-" * 50)
        if not self._products:
            print("There are no items in the inventory.")
            return
        for product in self._products:
            self.show_product_details(product)
        print("-" * 50)

    def load_products(self, products: list[dict[str, str | float | int]], suppliers: list[Supplier]):
        for item in products:
            supplier = None
            for s in suppliers:
                if s.supplier_id == item["supplier"]:
                    supplier = s
                    break
            if supplier is None:
                raise ValueError(f"Supplier with ID {item['supplier']} not found.")
            product_type = item.get("type")
            if product_type == "physical":
                product = ProductFactory.create("physical", str(item["id"]), str(item["name"]),
                                                float(item["price"]), int(item["stock"]),
                                                supplier, weight=float(item["weight"]))
                self.add_product(product)
            elif product_type == "digital":
                product = ProductFactory.create("digital", str(item["id"]), str(item["name"]),
                                                float(item["price"]), int(item["stock"]),
                                                supplier, download_size=float(item["download_size"]))
                self.add_product(product)

    def to_dict(self) -> dict[str, list[dict[str, str | float | int]]]:
        products: list[dict[str, str | float | int]] = []
        for product in self._products:
            products.append(product.to_dict())
        return {"products": products}