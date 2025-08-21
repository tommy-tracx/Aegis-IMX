"""Schema registry using Pydantic models."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MarketTick(BaseModel):
    id: int
    symbol: str
    price: float
    volume: int
    event_time: datetime


class Transaction(BaseModel):
    id: int
    account_id: int
    symbol: str
    quantity: int
    price: float
    event_time: datetime


class Position(BaseModel):
    id: int
    account_id: int
    symbol: str
    quantity: int
    as_of: datetime
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    end_at: Optional[datetime] = None
    is_current: bool = True
