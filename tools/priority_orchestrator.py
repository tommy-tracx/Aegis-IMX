#!/usr/bin/env python3
"""Compute MVP priorities and update development_queue.md.

Priority formula:
Priority = (MV * 0.4) + (TF * 0.3) + (TTM * 0.2) + (SI * 0.1)

Usage:
  python tools/priority_orchestrator.py --print
  python tools/priority_orchestrator.py --update
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

WEIGHTS = {"MV": 0.4, "TF": 0.3, "TTM": 0.2, "SI": 0.1}

@dataclass
class Slice:
    name: str
    MV: float
    TF: float
    TTM: float
    SI: float
    priority: float | None = None

    def compute_priority(self) -> float:
        self.priority = (
            self.MV * WEIGHTS["MV"]
            + self.TF * WEIGHTS["TF"]
            + self.TTM * WEIGHTS["TTM"]
            + self.SI * WEIGHTS["SI"]
        )
        return self.priority

def load_metrics(path: Path) -> List[Slice]:
    data = json.loads(path.read_text())
    return [Slice(**item) for item in data["slices"]]

def build_table(slices: List[Slice]) -> str:
    for s in slices:
        s.compute_priority()
    slices.sort(key=lambda s: s.priority, reverse=True)

    header = ["Rank", "Slice", "MV", "TF", "TTM", "SI", "Priority"]
    sep = "|" + "------|" * len(header)
    lines = ["| " + " | ".join(header) + " |", sep]

    for idx, s in enumerate(slices, 1):
        lines.append(
            f"| {idx} | {s.name} | {s.MV} | {s.TF} | {s.TTM} | {s.SI} | {s.priority:.1f} |"
        )
    return "\n".join(lines)

def update_development_queue(md_path: Path, table_md: str) -> None:
    lines = md_path.read_text().splitlines()
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("| Rank |"):
            start = i
            break
    if start is None:
        raise RuntimeError("Table start not found in development_queue.md")
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    new_lines = lines[:start] + table_md.splitlines() + lines[end:]
    md_path.write_text("\n".join(new_lines) + "\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="Compute MVP priorities")
    parser.add_argument(
        "--metrics",
        default=Path("shared/mvp_metrics.json"),
        type=Path,
        help="Path to metrics JSON file",
    )
    parser.add_argument(
        "--queue",
        default=Path("development_queue.md"),
        type=Path,
        help="Path to development queue markdown",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the development queue file with computed table",
    )
    args = parser.parse_args()

    slices = load_metrics(args.metrics)
    table = build_table(slices)
    if args.update:
        update_development_queue(args.queue, table)
    else:
        print(table)

if __name__ == "__main__":
    main()
