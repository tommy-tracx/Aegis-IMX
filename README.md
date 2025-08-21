# Aegis-IMX Risk Engine

This project provides a minimal risk engine capable of running Value-at-Risk (VaR) computations via a FastAPI service.

## Features
- Parametric and Historical VaR calculations using Polars
- FastAPI endpoints for executing risk runs and fetching results
- In-memory caching of run results
- Basic unit tests with `pytest`

## API
- `POST /risk/run` with JSON body `{portfolio_id, as_of, method, positions?, returns?}`
  - `positions` required for `parametric` method
  - `returns` required for `historical` method
- `GET /risk/results/{run_id}` retrieves cached results

## Development
```bash
pip install -r requirements.txt  # if available
uvicorn risk_engine.api:app --reload
pytest
```
=======
# Aegis-IMX

Enterprise-grade reference implementation for institutional investment management.  
Includes lightweight Order & Execution Management (OMS/EMS) demo and a minimal Portfolio Service built with FastAPI.

---

## Features
- **OMS/EMS Demo** – Basic order creation, execution, and management.
- **Portfolio Service** – CRUD operations, role-based access control, and position aggregation.
- **Modular Architecture** – Microservices, APIs, and shared libraries.
- **Enterprise Foundations** – MLOps pipelines, Delta/Iceberg data lake, and security integrations.

---

## Repository Layout
- `infra/` – Terraform, Helm charts, GitHub Actions CI/CD
- `gateway/` – API Gateway with OPA plugin
- `idp/` – OIDC identity provider
- `lake/` – Delta/Iceberg lakehouse
- `services/` – Core domain microservices
- `ui/` – Next.js/React front-end
- `mlops/` – Model registry and feature pipelines
- `shared/` – Libraries and schemas
- `tools/` – Orchestration and utilities
- `tests/` – E2E, chaos, and performance tests
- `docs/` – Architecture, threat models, data classification, cost models

---

## Setup

```bash
pip install -r requirements.txt

Run OMS/EMS demo locally:

uvicorn app.main:app --reload


⸻

Testing

pytest


⸻

Documentation

See /docs for:
	•	Architecture overview
	•	Threat model
	•	Data classification

