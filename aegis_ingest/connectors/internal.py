"""Internal connectors for positions, transactions, and order fills."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pyspark.sql import SparkSession

from .base import BaseConnector, IngestionConfig

InternalType = Literal["positions", "transactions", "order_fills"]


class InternalConnector(BaseConnector):
    """Connector for internal data sources."""

    def __init__(self, spark: SparkSession, data_type: InternalType, path: Path, fmt: str = "csv") -> None:
        config = IngestionConfig(source_path=path, format=fmt)
        super().__init__(spark, config)
        self.data_type = data_type
