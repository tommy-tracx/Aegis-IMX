from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Portfolio(Base):
    """Represents an investment portfolio."""

    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    positions = relationship(
        "Position", back_populates="portfolio", cascade="all, delete-orphan"
    )


class Position(Base):
    """Represents an individual holding within a portfolio."""

    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    instrument = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    sector = Column(String, nullable=True)

    portfolio = relationship("Portfolio", back_populates="positions")
