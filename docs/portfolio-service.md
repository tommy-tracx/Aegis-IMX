# Portfolio Service Guide

FastAPI microservice managing investment portfolios and positions.

## Features
- CRUD operations for portfolios with optional positions.
- Role-based access control via `X-Role` header.
- Aggregated position view grouped by instrument.
- SQLite persistence with SQLAlchemy models.

## Roles
Allowed roles: `PM`, `Risk`, `Ops`, `Compliance`, `Client`.

## Key Endpoints
| Method | Path | Description | Allowed Roles |
| ------ | ---- | ----------- | ------------- |
| `POST` | `/portfolios` | Create portfolio | PM, Ops, Compliance |
| `GET` | `/portfolios/{id}` | Retrieve portfolio by id | All roles |
| `PUT` | `/portfolios/{id}` | Update portfolio name | PM, Ops, Compliance |
| `DELETE` | `/portfolios/{id}` | Remove portfolio | Ops |
| `GET` | `/portfolios/{id}/positions` | Aggregated positions | All roles |

## Running the Service
```bash
uvicorn portfolio_service.main:app --reload
```

## Data Model
Portfolio and Position models are defined in [`src/portfolio_service/models.py`](../src/portfolio_service/models.py) and Pydantic schemas in [`src/portfolio_service/schemas.py`](../src/portfolio_service/schemas.py).

## Testing
Run unit tests:
```bash
pytest tests/test_portfolio_api.py::test_create_portfolio
```
