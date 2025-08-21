from datetime import datetime, timezone
from typing import Dict
from .models import Order, Event


def publish(order: Order, event_type: str, details: Dict[str, str] | None = None) -> Event:
    """Publish an event to an order's audit trail."""
    event = Event(
        type=event_type,
        timestamp=datetime.now(timezone.utc),
        details=details or {},
    )
    order.events.append(event)
    return event
