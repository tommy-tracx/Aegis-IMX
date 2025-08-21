"""Business logic for performance calculations."""

from __future__ import annotations

import logging
import uuid
from typing import Dict, Iterable, List

from .models import PerformanceResult, PerformanceRunRequest, ReturnAttribution

logger = logging.getLogger(__name__)

# In-memory run store for demo purposes
_RUN_STORE: Dict[str, PerformanceResult] = {}


def _geometric_link(returns: Iterable[float]) -> float:
    """Compute geometric linked return (time-weighted)."""
    result = 1.0
    for r in returns:
        result *= 1 + r
    return result - 1


def _irr(cash_flows: List[float]) -> float:
    """Approximate internal rate of return using Newton-Raphson."""
    if not any(cf < 0 for cf in cash_flows) or not any(cf > 0 for cf in cash_flows):
        return 0.0
    guess = 0.1
    for _ in range(100):
        npv = sum(cf / (1 + guess) ** i for i, cf in enumerate(cash_flows))
        derivative = -sum(i * cf / (1 + guess) ** (i + 1) for i, cf in enumerate(cash_flows))
        if derivative == 0:
            break
        next_guess = guess - npv / derivative
        if abs(next_guess - guess) < 1e-6:
            return next_guess
        guess = next_guess
    return guess


def _brinson_stub() -> ReturnAttribution:
    """Return neutral attribution placeholder."""
    return ReturnAttribution(allocation=0.0, selection=0.0, interaction=0.0)


def run_performance(request: PerformanceRunRequest) -> PerformanceResult:
    """Execute performance run and store result in memory."""
    twr = _geometric_link(request.returns)
    irr = _irr(request.cash_flows)
    attribution = _brinson_stub()
    result = PerformanceResult(
        portfolio_id=request.portfolio_id,
        period=request.period,
        time_weighted_return=twr,
        money_weighted_return=irr,
        attribution=attribution,
        as_of=max(request.dates),
    )
    run_id = str(uuid.uuid4())
    _RUN_STORE[run_id] = result
    logger.info("Stored performance run %s", run_id)
    return result, run_id


def get_run(run_id: str) -> PerformanceResult:
    """Retrieve previously computed performance run."""
    if run_id not in _RUN_STORE:
        raise KeyError(f"run_id {run_id} not found")
    return _RUN_STORE[run_id]
