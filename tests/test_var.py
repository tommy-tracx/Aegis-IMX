import polars as pl
import pytest

from risk_engine.engine import RiskEngine
from risk_engine.models import PortfolioSnapshot, parametric_var, historical_var


def test_parametric_var_simple():
    positions = pl.DataFrame([
        {"asset": "A", "value": 100, "factor1": 1.0},
        {"asset": "B", "value": 200, "factor1": 0.5},
    ])
    snapshot = PortfolioSnapshot(positions)
    var = parametric_var(snapshot, conf_level=0.95)
    assert var > 0


def test_historical_var_simple():
    returns = pl.DataFrame({"return": [-0.01, 0.02, -0.03, 0.01]})
    var = historical_var(returns, conf_level=0.95)
    assert var == pytest.approx(0.03)


def test_engine_run_risk_historical():
    returns = pl.DataFrame({"return": [-0.01, 0.02, -0.03, 0.01]})
    engine = RiskEngine()
    run_id = engine.run_risk(returns=returns, method="historical")
    result = engine.get_results(run_id)
    assert result["var"] == pytest.approx(0.03)
