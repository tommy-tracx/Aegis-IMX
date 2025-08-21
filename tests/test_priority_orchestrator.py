import json
from pathlib import Path

import sys
from pathlib import Path

# Ensure project root is on path so `tools` package can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

from tools.priority_orchestrator import build_table, load_metrics


def test_compute_priority(tmp_path: Path) -> None:
    data = {
        "slices": [
            {"name": "A", "MV": 5, "TF": 4, "TTM": 3, "SI": 5},
            {"name": "B", "MV": 3, "TF": 3, "TTM": 2, "SI": 4},
        ]
    }
    metrics_path = tmp_path / "metrics.json"
    metrics_path.write_text(json.dumps(data))
    slices = load_metrics(metrics_path)
    table = build_table(slices)
    # Check table contains names and computed priorities
    assert "A" in table and "B" in table
    # First slice priority should be 4.3
    assert any("4.3" in row for row in table.splitlines())
