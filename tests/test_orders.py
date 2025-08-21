import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pretrade_block():
    resp = client.post(
        "/orders",
        json={"symbol": "AAPL", "side": "BUY", "quantity": 2000, "price": 10.0},
    )
    assert resp.status_code == 400


def create_order():
    resp = client.post(
        "/orders",
        json={"symbol": "AAPL", "side": "BUY", "quantity": 100, "price": 10.0},
    )
    assert resp.status_code == 200
    return resp.json()


def test_allocation_rules_and_trace():
    order = create_order()
    order_id = order["id"]
    route_resp = client.post(
        f"/orders/{order_id}/route", json={"venue": "SIM1", "quantity": 100}
    )
    assert route_resp.status_code == 200
    alloc_resp = client.post(
        f"/orders/{order_id}/allocate",
        json={
            "allocations": [
                {"account": "ACC1", "quantity": 50},
                {"account": "ACC2", "quantity": 50},
            ]
        },
    )
    assert alloc_resp.status_code == 200
    data = alloc_resp.json()
    assert [e["type"] for e in data["events"]] == [
        "order_created.v1",
        "pretrade_passed.v1",
        "execution_fill.v1",
    ]


def test_allocation_mismatch():
    order = create_order()
    order_id = order["id"]
    route_resp = client.post(
        f"/orders/{order_id}/route", json={"venue": "SIM1", "quantity": 100}
    )
    assert route_resp.status_code == 200
    bad_alloc = client.post(
        f"/orders/{order_id}/allocate",
        json={
            "allocations": [
                {"account": "ACC1", "quantity": 60},
                {"account": "ACC2", "quantity": 50},
            ]
        },
    )
    assert bad_alloc.status_code == 400
