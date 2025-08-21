"""Streaming ingestion using Kafka and Spark Structured Streaming."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType

from ..quality.expectations import run_expectations
from ..security.encryption import encrypt_columns
from ..lineage.tracker import LineageTracker


class StreamingPipeline:
    """Kafka -> Delta streaming pipeline with watermarking and dedup."""

    def __init__(
        self,
        spark: SparkSession,
        base_path: Path,
        lineage: Optional[LineageTracker] = None,
    ) -> None:
        self.spark = spark
        self.base_path = base_path
        self.lineage = lineage or LineageTracker()

    def run(
        self,
        name: str,
        kafka_topic: str,
        schema: StructType,
        expectations: Optional[dict] = None,
        pii_columns: Optional[list[str]] = None,
        watermark: str = "10 minutes",
    ) -> None:
        """Start streaming ingestion from Kafka."""
        df = (
            self.spark.readStream.format("kafka")
            .option("subscribe", kafka_topic)
            .option("kafka.bootstrap.servers", "localhost:9092")
            .load()
        )
        parsed = (
            df.selectExpr("CAST(value AS STRING) as json")
            .select(from_json("json", schema).alias("data"))
            .select("data.*")
            .withColumn("event_time", to_timestamp(col("event_time")))
            .withWatermark("event_time", watermark)
            .dropDuplicates(["id", "event_time"])
        )
        if expectations:
            run_expectations(parsed, expectations)
        if pii_columns:
            parsed = encrypt_columns(parsed, pii_columns)

        query = (
            parsed.writeStream.format("delta")
            .option("checkpointLocation", str(self.base_path / "chk" / name))
            .option("path", str(self.base_path / "bronze" / name))
            .outputMode("append")
            .start()
        )
        query.awaitTermination(5)
        self.lineage.emit_stream(name, str(self.base_path / "bronze" / name))
