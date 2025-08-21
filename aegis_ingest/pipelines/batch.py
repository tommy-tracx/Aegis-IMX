"""Batch ingestion pipelines using Parquet files."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import current_timestamp

from ..connectors.base import BaseConnector
from ..quality.expectations import run_expectations
from ..quality.scd import apply_scd2
from ..security.encryption import encrypt_columns
from ..lineage.tracker import LineageTracker


class BatchPipeline:
    """Bronze -> Silver -> Gold batch pipeline."""

    def __init__(
        self,
        spark: SparkSession,
        base_path: Path,
        lineage: Optional[LineageTracker] = None,
    ) -> None:
        self.spark = spark
        self.base_path = base_path
        self.lineage = lineage or LineageTracker()

    def _write(self, df: DataFrame, layer: str, table: str) -> DataFrame:
        dest = self.base_path / layer / table
        df.write.mode("append").parquet(str(dest))
        return self.spark.read.parquet(str(dest))

    def run(
        self,
        name: str,
        connector: BaseConnector,
        transformations: Optional[Callable[[DataFrame], DataFrame]] = None,
        expectations: Optional[dict] = None,
        pii_columns: Optional[list[str]] = None,
        encryption_key: bytes | None = None,
        scd2_keys: Optional[list[str]] = None,
        effective_date_col: str | None = None,
    ) -> None:
        """Execute pipeline for a given connector.

        Parameters
        ----------
        name:
            Destination table name.
        connector:
            Data source connector.
        transformations:
            Optional function to transform the dataframe between Bronze and Silver.
        expectations:
            Column expectations for quality checks.
        pii_columns:
            Columns to encrypt using Fernet symmetric encryption.
        encryption_key:
            Key used for encryption if ``pii_columns`` are provided.
        scd2_keys:
            Keys identifying unique entities for SCD Type 2 tracking.
        effective_date_col:
            Column representing the effective date for SCD Type 2 tracking.
        """
        df = connector.read().withColumn("ingest_ts", current_timestamp())
        if expectations:
            run_expectations(df, expectations)
        bronze = self._write(df, "bronze", name)

        silver_df = bronze.dropDuplicates()
        if transformations:
            silver_df = transformations(silver_df)
        if scd2_keys and effective_date_col:
            silver_df = apply_scd2(silver_df, scd2_keys, effective_date_col)
        if pii_columns:
            silver_df = encrypt_columns(silver_df, pii_columns, key=encryption_key)
        silver = self._write(silver_df, "silver", name)

        gold_df = silver
        gold = self._write(gold_df, "gold", name)

        self.lineage.emit(name, ["bronze", "silver", "gold"])
