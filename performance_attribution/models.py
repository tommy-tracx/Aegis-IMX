"""Pydantic models for Performance & Attribution service."""

from datetime import date
from typing import List

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PerformanceRunRequest(BaseModel):
    """Request payload to trigger a performance run."""

    portfolio_id: str = Field(..., description="Unique portfolio identifier")
    period: str = Field(..., description="ISO period string, e.g. '2023Q1'")
    returns: List[float] = Field(..., description="Series of periodic returns")
    cash_flows: List[float] = Field(..., description="Cash flow amounts for IRR")
    dates: List[date] = Field(..., description="Dates corresponding to returns")

    @field_validator("returns", "cash_flows", "dates")
    @classmethod
    def non_empty(cls, v: List) -> List:
        if not v:
            raise ValueError("Sequence must not be empty")
        return v

    @field_validator("dates")
    @classmethod
    def returns_date_length(cls, v: List[date], info: ValidationInfo) -> List[date]:
        returns = info.data.get("returns") if info.data else None
        if returns is not None and len(v) != len(returns):
            raise ValueError("dates and returns must be same length")
        return v


class PerformanceRunResponse(BaseModel):
    """Response after scheduling a performance run."""

    run_id: str = Field(..., description="Server-generated run identifier")


class ReturnAttribution(BaseModel):
    """Simple attribution container."""

    allocation: float
    selection: float
    interaction: float


class PerformanceResult(BaseModel):
    """Result payload for completed performance run."""

    portfolio_id: str
    period: str
    time_weighted_return: float
    money_weighted_return: float
    attribution: ReturnAttribution
    as_of: date

    def to_dict(self) -> dict:
        """Return dictionary representation for export convenience."""
        return self.model_dump()
