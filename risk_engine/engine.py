"""Risk engine orchestrating risk runs and caching results."""
from __future__ import annotations

import uuid
from typing import Dict, Optional

import polars as pl

from .models import PortfolioSnapshot, parametric_var, historical_var


class RiskEngine:
    """Orchestrates risk calculations and stores results."""

    def __init__(self) -> None:
        self._cache: Dict[str, Dict[str, float]] = {}

    def run_risk(
        self,
        snapshot: Optional[PortfolioSnapshot] = None,
        *,
        returns: Optional[pl.DataFrame] = None,
        method: str = "parametric",
    ) -> str:
        """Execute risk calculation and cache result.

        Args:
            snapshot: PortfolioSnapshot of positions for parametric VaR.
            returns: DataFrame of historical returns for historical VaR.
            method: Risk method, "parametric" or "historical".

        Returns:
            run_id identifying stored results.

        Raises:
            ValueError: If required inputs for the chosen method are missing.
        """
        if method == "parametric":
            if snapshot is None:
                raise ValueError("snapshot required for parametric VaR")
            var = parametric_var(snapshot)
        elif method == "historical":
            if returns is None:
                raise ValueError("returns required for historical VaR")
            var = historical_var(returns)
        else:
            raise ValueError(f"Unknown method {method}")

        run_id = str(uuid.uuid4())
        self._cache[run_id] = {"var": var}
        return run_id

    def get_results(self, run_id: str) -> Dict[str, float]:
        """Retrieve cached results."""
        return self._cache[run_id]


__all__ = ["RiskEngine"]
