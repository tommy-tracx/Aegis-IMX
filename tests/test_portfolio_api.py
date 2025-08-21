import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from portfolio_service.main import app
from portfolio_service.db import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_and_aggregate_portfolio():
    response = client.post(
        "/portfolios",
        json={
            "name": "Alpha",
            "positions": [
                {"instrument": "AAPL", "quantity": 50},
                {"instrument": "AAPL", "quantity": 30},
            ],
        },
        headers={"X-Role": "PM"},
    )
    assert response.status_code == 200, response.text
    portfolio_id = response.json()["id"]

    response = client.get(f"/portfolios/{portfolio_id}", headers={"X-Role": "Client"})
    assert response.status_code == 200

    response = client.get(
        f"/portfolios/{portfolio_id}/positions", headers={"X-Role": "Risk"}
    )
    assert response.status_code == 200
    assert response.json() == [{"instrument": "AAPL", "quantity": 80}]


def test_create_forbidden_for_client():
    response = client.post(
        "/portfolios",
        json={"name": "Beta", "positions": []},
        headers={"X-Role": "Client"},
    )
    assert response.status_code == 403


def test_delete_requires_ops_role():
    response = client.post(
        "/portfolios",
        json={"name": "Gamma", "positions": []},
        headers={"X-Role": "PM"},
    )
    portfolio_id = response.json()["id"]

    response = client.delete(f"/portfolios/{portfolio_id}", headers={"X-Role": "PM"})
    assert response.status_code == 403

    response = client.delete(f"/portfolios/{portfolio_id}", headers={"X-Role": "Ops"})
    assert response.status_code == 200
