import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from compliance import Policy, ComplianceEngine
import app


def test_policy_signature_and_loading(tmp_path):
    policy = Policy.load("policies/policy_v1.yaml")
    policy.sign("secret")
    assert policy.signature
    # Dump and reload to ensure serialization works
    path = tmp_path / "policy.yaml"
    policy.dump(path)
    loaded = Policy.load(path)
    assert loaded.signature == policy.signature


def test_pretrade_pass_and_fail():
    policy = Policy.load("policies/policy_v1.yaml")
    engine = ComplianceEngine(policy)
    order = {"symbol": "AAPL", "quantity": 10, "issuer": "Apple"}
    portfolio = {"positions": {"AAPL": 5}, "restricted_list": [], "issuer_limits": {"Apple": 100}}
    passed, _ = engine.pre_trade(order, portfolio)
    assert passed
    order2 = {"symbol": "TSLA", "quantity": 10, "issuer": "Tesla"}
    portfolio2 = {"positions": {}, "restricted_list": ["TSLA"], "issuer_limits": {"Tesla": 100}}
    passed2, _ = engine.pre_trade(order2, portfolio2)
    assert not passed2


def test_api_endpoints():
    client = TestClient(app.app)
    payload = {
        "order": {"symbol": "AAPL", "quantity": 10, "issuer": "Apple"},
        "portfolio_state": {"positions": {"AAPL": 5}, "restricted_list": [], "issuer_limits": {"Apple": 100}}
    }
    resp = client.post("/compliance/pretrade", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "eval_id" in data
    eval_id = data["eval_id"]
    exp_resp = client.get(f"/compliance/explanations/{eval_id}")
    assert exp_resp.status_code == 200
