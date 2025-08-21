# Aegis-IMX

Lakehouse ingestion framework for market, reference, and internal data. Provides
connectors, batch and streaming pipelines, schema registry, quality checks,
security utilities, and lineage tracking.

### Features

- Configurable connectors for market, reference, and internal datasets.
- Batch pipeline with Bronze→Silver→Gold stages, optional column encryption, and SCD2 tracking.
- Streaming ingestion from Kafka with watermarking and deduplication.
- Pydantic schemas and lightweight data quality expectations.
- JSON lineage events for simple audit trails.

## Usage

```python
from pathlib import Path

from cryptography.fernet import Fernet
from pyspark.sql import SparkSession

from aegis_ingest.connectors.internal import InternalConnector
from aegis_ingest.pipelines.batch import BatchPipeline

spark = (
    SparkSession.builder.appName("demo").master("local[*]")
    .config("spark.sql.shuffle.partitions", "1")
    .getOrCreate()
)

base_path = Path("/tmp/lakehouse")
pipeline = BatchPipeline(spark, base_path)
connector = InternalConnector(spark, "positions", Path("data/internal/positions.csv"))

key = Fernet.generate_key()
pipeline.run(
    name="positions",
    connector=connector,
    pii_columns=["account_id"],
    encryption_key=key,
    scd2_keys=["id"],
    effective_date_col="as_of",
)
```

### Encryption

Sensitive columns can be encrypted by supplying a Fernet key either via the
``PII_ENCRYPTION_KEY`` environment variable or the ``encryption_key`` argument
to the batch pipeline.

## Running Tests

```bash
pytest -q
```
