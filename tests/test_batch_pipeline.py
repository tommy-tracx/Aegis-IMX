from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cryptography.fernet import Fernet
from pyspark.sql import SparkSession
from pyspark.sql.types import BinaryType
from pyspark.sql import functions as F

from aegis_ingest.connectors.internal import InternalConnector
from aegis_ingest.pipelines.batch import BatchPipeline


def spark_session():
    return (
        SparkSession.builder.appName("test").master("local[*]")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )


def test_positions_batch(tmp_path):
    spark = spark_session()
    base = tmp_path / "lakehouse"
    pipeline = BatchPipeline(spark, base)
    connector = InternalConnector(spark, "positions", Path("data/internal/positions.csv"))
    expectations = {"id": {"non_null": True, "unique": False}}

    key = Fernet.generate_key()
    pipeline.run(
        name="positions",
        connector=connector,
        expectations=expectations,
        pii_columns=["account_id"],
        encryption_key=key,
        scd2_keys=["id"],
        effective_date_col="as_of",
    )

    gold_path = base / "gold" / "positions"
    df = spark.read.parquet(str(gold_path))
    assert df.count() == 3
    assert "account_id" in df.columns
    assert isinstance(df.schema["account_id"].dataType, BinaryType)

    row = df.filter((F.col("id") == 1) & (F.col("as_of") == "2025-01-01")).collect()[0]
    assert row.is_current is False
    assert str(row.end_at) == "2025-01-02 00:00:00"
    current_row = df.filter((F.col("id") == 1) & (F.col("as_of") == "2025-01-02")).collect()[0]
    assert current_row.is_current is True
    assert current_row.end_at is None

    spark.stop()
