"""Base connector abstractions for ingestion sources."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame, SparkSession

LOGGER = logging.getLogger(__name__)


@dataclass
class IngestionConfig:
    """Configuration for ingestion connectors."""

    source_path: Path
    format: str = "csv"  # csv or parquet
    options: dict[str, Any] = field(default_factory=dict)


class BaseConnector:
    """Base class for all connectors."""

    def __init__(self, spark: SparkSession, config: IngestionConfig) -> None:
        self.spark = spark
        self.config = config

    def read(self) -> DataFrame:
        """Read source data into a :class:`pyspark.sql.DataFrame`."""

        if not self.config.source_path.exists():
            msg = f"source path {self.config.source_path} does not exist"
            raise FileNotFoundError(msg)

        reader = self.spark.read
        fmt = self.config.format
        if fmt == "csv":
            reader = reader.option("header", True)
        for k, v in self.config.options.items():
            reader = reader.option(k, v)

        LOGGER.info("Loading %s with format %s", self.config.source_path, fmt)
        return reader.format(fmt).load(str(self.config.source_path))
