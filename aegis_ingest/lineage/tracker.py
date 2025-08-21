"""Simple lineage tracker using JSON events."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class LineageEvent:
    dataset: str
    layers: Iterable[str]
    timestamp: str = datetime.utcnow().isoformat()


class LineageTracker:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path("lineage_events.jsonl")

    def emit(self, dataset: str, layers: Iterable[str]) -> None:
        event = LineageEvent(dataset, layers)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(event)) + "\n")

    def emit_stream(self, dataset: str, location: str) -> None:
        event = {"dataset": dataset, "location": location, "timestamp": datetime.utcnow().isoformat()}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event) + "\n")
