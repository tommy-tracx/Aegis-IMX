"""SCD Type 2 utilities for tracking slowly changing dimensions."""
from __future__ import annotations

from typing import Iterable

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def apply_scd2(
    df: DataFrame,
    keys: Iterable[str],
    effective_date_col: str,
) -> DataFrame:
    """Apply SCD Type 2 semantics to ``df``.

    Parameters
    ----------
    df:
        Incoming dataframe containing new records.
    keys:
        Columns that uniquely identify an entity.
    effective_date_col:
        Column indicating when the record became effective.

    Returns
    -------
    DataFrame
        Dataframe with ``end_at`` and ``is_current`` columns added.
    """
    order_col = F.col(effective_date_col).cast("timestamp")
    w = Window.partitionBy(*keys).orderBy(order_col)
    end_at = F.lead(order_col).over(w)
    df = df.withColumn("end_at", end_at).withColumn("is_current", end_at.isNull())
    return df
