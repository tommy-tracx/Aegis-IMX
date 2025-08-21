"""Risk model implementations for VaR and other measures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import polars as pl
import numpy as np
from scipy.stats import norm


@dataclass
class PortfolioSnapshot:
    """Represents portfolio positions with factors and exposures."""
    positions: pl.DataFrame  # columns: asset, value, factor1, factor2, ...


def parametric_var(snapshot: PortfolioSnapshot, conf_level: float = 0.99) -> float:
    """Compute Parametric VaR using variance-covariance approach.

    Args:
        snapshot: PortfolioSnapshot containing asset values and factor sensitivities.
        conf_level: Confidence level for VaR.

    Returns:
        Value at Risk at the given confidence level.
    """
    factors = [col for col in snapshot.positions.columns if col not in {"asset", "value"}]
    exposures = snapshot.positions.select(factors).to_numpy()
    values = snapshot.positions["value"].to_numpy()

    # Assume factors are standardized and independent for simplicity
    # Portfolio variance = sum(exposures^2 * value^2)
    var = np.sum((exposures * values[:, None]) ** 2)
    sigma = np.sqrt(var)
    z = norm.ppf(conf_level)
    return float(z * sigma)


def historical_var(returns: pl.DataFrame, conf_level: float = 0.99) -> float:
    """Compute Historical VaR from a DataFrame of portfolio returns."""
    quantile = 1 - conf_level
    return float(-returns.select(pl.col("return")).quantile(quantile)[0, 0])


__all__ = ["PortfolioSnapshot", "parametric_var", "historical_var"]
