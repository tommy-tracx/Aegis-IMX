"""Result exporters for various formats."""

import csv
from io import StringIO
from typing import Iterable, List

from .models import PerformanceResult

try:  # optional dependency
    import pyarrow as pa
    import pyarrow.parquet as pq
except Exception:  # pragma: no cover - pyarrow optional
    pa = pq = None  # type: ignore


def export_csv(results: Iterable[PerformanceResult]) -> str:
    """Return CSV string for provided results."""
    items: List[PerformanceResult] = list(results)
    if not items:
        return ""
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(items[0].to_dict().keys()))
    writer.writeheader()
    for r in items:
        writer.writerow(r.to_dict())
    return buffer.getvalue()


def export_parquet(results: Iterable[PerformanceResult]) -> bytes:
    """Return Parquet bytes for provided results."""
    items = list(results)
    if not items:
        return b""
    if pa is None or pq is None:  # pragma: no cover - optional
        raise RuntimeError("pyarrow not installed")
    table = pa.Table.from_pylist([r.to_dict() for r in items])
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)
    return buffer.getvalue().to_pybytes()
