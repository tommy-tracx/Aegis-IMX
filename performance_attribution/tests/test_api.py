"""API tests using FastAPI TestClient."""

from fastapi.testclient import TestClient

from performance_attribution import create_app


client = TestClient(create_app())


def test_perf_run_and_results():
    payload = {
        "portfolio_id": "P1",
        "period": "2023Q1",
        "returns": [0.1, 0.05],
        "cash_flows": [-100, 60, 60],
        "dates": ["2023-01-01", "2023-03-31"],
    }
    res = client.post("/perf/run", json=payload)
    assert res.status_code == 200
    run_id = res.json()["run_id"]

    res2 = client.get(f"/perf/results/{run_id}")
    assert res2.status_code == 200
    body = res2.json()
    assert body["portfolio_id"] == "P1"
