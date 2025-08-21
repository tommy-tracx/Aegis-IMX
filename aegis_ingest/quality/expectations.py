"""Simple data quality checks inspired by Great Expectations."""
from __future__ import annotations

from typing import Dict

from pyspark.sql import DataFrame


def run_expectations(df: DataFrame, expectations: Dict[str, dict], sample_rows: int = 1000) -> None:
    """Validate ``DataFrame`` columns according to provided expectations.

    Parameters
    ----------
    df:
        Spark DataFrame to validate.
    expectations:
        Mapping of column names to expectation definitions.
    sample_rows:
        Number of rows to convert to pandas for lightweight checks.

    Raises
    ------
    ValueError
        If any expectation is violated.
    """

    pdf = df.limit(sample_rows).toPandas()
    for column, checks in expectations.items():
        if checks.get("non_null") and pdf[column].isnull().any():
            raise ValueError(f"{column} contains nulls")
        if checks.get("unique") and not pdf[column].is_unique:
            raise ValueError(f"{column} contains duplicates")
