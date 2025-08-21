"""Market data connectors for equities, fixed income, options, FX."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pyspark.sql import SparkSession

from .base import BaseConnector, IngestionConfig

MarketType = Literal["equities", "fixed_income", "options", "fx"]


class MarketConnector(BaseConnector):
    """Connector for vendor-provided market data."""

    def __init__(self, spark: SparkSession, market: MarketType, path: Path, fmt: str = "csv") -> None:
        config = IngestionConfig(source_path=path, format=fmt)
        super().__init__(spark, config)
        self.market = market
