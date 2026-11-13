from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Apply the discount to the given total and return the discounted amount."""
        pass

class NoDiscount(DiscountStrategy):
    """Strategy that applies no discount."""

    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    """Strategy that applies a percentage discount."""

    def __init__(self, percentage: float):
        """
        Initialize with a percentage discount.

        Args:
            percentage: The percentage to discount (e.g., 10 for 10%)
        """
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)

class BulkDiscount(DiscountStrategy):
    """Strategy that applies a fixed discount if total meets threshold."""

    def __init__(self, threshold: float, amount: float):
        """
        Initialize with a threshold and discount amount.

        Args:
            threshold: The minimum total required to apply the discount
            amount: The fixed amount to discount
        """
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return total - self.amount
        return total

class StudentDiscount(DiscountStrategy):
    """Strategy that applies a 5% student discount."""

    def apply(self, total: float) -> float:
        return total * 0.95
