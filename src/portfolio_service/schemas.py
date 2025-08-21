from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PositionBase(BaseModel):
    instrument: str
    quantity: int
    sector: Optional[str] = None


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PortfolioBase(BaseModel):
    name: str


class PortfolioCreate(PortfolioBase):
    positions: List[PositionCreate] = []


class PortfolioRead(PortfolioBase):
    id: int
    positions: List[PositionRead] = []

    model_config = ConfigDict(from_attributes=True)
