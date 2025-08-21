from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(str, Enum):
    NEW = "NEW"
    ROUTED = "ROUTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"


class Event(BaseModel):
    type: str
    timestamp: datetime
    details: Dict[str, str] = Field(default_factory=dict)


class ChildOrder(BaseModel):
    id: int
    venue: str
    quantity: int
    filled_quantity: int = 0


class Allocation(BaseModel):
    account: str
    quantity: int


class Order(BaseModel):
    id: int
    symbol: str
    side: OrderSide
    quantity: int
    price: float
    status: OrderStatus = OrderStatus.NEW
    filled_quantity: int = 0
    events: List[Event] = Field(default_factory=list)
    child_orders: List[ChildOrder] = Field(default_factory=list)
    allocations: List[Allocation] = Field(default_factory=list)
