"""Unit tests for performance service."""

from datetime import date

from performance_attribution.models import PerformanceRunRequest
from performance_attribution.service import _geometric_link, _irr, get_run, run_performance


def test_geometric_link():
    assert abs(_geometric_link([0.1, -0.05]) - 0.045) < 1e-6


def test_irr():
    cf = [-100, 60, 60]
    irr = _irr(cf)
    assert 0 < irr < 1


def test_run_and_get():
    req = PerformanceRunRequest(
        portfolio_id="P1",
        period="2023Q1",
        returns=[0.1, 0.05],
        cash_flows=[-100, 60, 60],
        dates=[date(2023, 1, 1), date(2023, 3, 31)],
    )
    result, run_id = run_performance(req)
    fetched = get_run(run_id)
    assert fetched.time_weighted_return == result.time_weighted_return
