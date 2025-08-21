"""Reference data connectors for instruments, calendars, benchmarks, curves."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pyspark.sql import SparkSession

from .base import BaseConnector, IngestionConfig

ReferenceType = Literal["instruments", "calendars", "benchmarks", "curves"]


class ReferenceConnector(BaseConnector):
    """Connector for reference data sources."""

    def __init__(self, spark: SparkSession, ref_type: ReferenceType, path: Path, fmt: str = "csv") -> None:
        config = IngestionConfig(source_path=path, format=fmt)
        super().__init__(spark, config)
        self.ref_type = ref_type
