from .models import Order


class ComplianceEngine:
    """Simple compliance engine performing pre-trade checks."""

    def __init__(self, max_quantity: int = 1000):
        self.max_quantity = max_quantity

    def validate(self, order: Order) -> None:
        """Validate order against compliance rules.

        Raises:
            ValueError: If any compliance rule is violated.
        """
        if order.quantity > self.max_quantity:
            raise ValueError("Order size exceeds limit")
