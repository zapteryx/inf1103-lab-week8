from product import Product
from order_line import OrderLine

class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_summary(self) -> None:
        print(f"--- Order Summary: {self.order_id} ---")
        if not self.order_lines:
            print("Order is empty.")
            return
        for line in self.order_lines:
            print(f"- Product: {line.product.name} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total: ${self.calculate_total():.2f}\n")