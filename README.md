# Aegis-IMX

Enterprise-grade reference implementation for institutional investment management, developed by **NeuralQuantum.ai**. The platform provides modular services including Order & Execution Management (OMS/EMS), Portfolio, Compliance, and Risk engines.

---

## Features

- **Order & Execution Management (OMS/EMS)**
  - FastAPI service with interactive endpoints.
- **Portfolio Service**
  - CRUD operations for portfolios.
  - Role-based access control (RBAC).
  - Position aggregation and reporting.
- **Compliance Engine**
  - Pre-trade and post-trade rule evaluation.
  - Policy versioning, signatures, and approvals.
  - Human-readable audit explanations.
- **Risk Engine**
  - Parametric and Historical Value-at-Risk (VaR) calculations using Polars.
  - FastAPI endpoints for risk runs and result retrieval.
  - In-memory caching of risk evaluation results.
- **Enterprise Architecture Foundations**
  - Modular microservices (OMS, Portfolio, Compliance, Risk).
  - Event-driven integration with Kafka/Redpanda.
  - Security via OIDC, OPA, and mTLS.
  - Lakehouse platform with Delta/Iceberg, Spark, and Flink.
  - MLOps pipelines and feature registry.

---

## Repository Layout

- `infra/` – Terraform, Helm, GitHub Actions CI/CD
- `gateway/` – API Gateway with OPA plugin
- `idp/` – OIDC identity provider
- `lake/` – Delta/Iceberg lakehouse
- `services/` – Core domain microservices (OMS, Portfolio, Compliance, Risk)
- `ui/` – Next.js/React front-end
- `mlops/` – Model registry and feature pipelines
- `shared/` – Common libraries and schemas
- `tools/` – Orchestration and developer utilities
- `tests/` – E2E, chaos, and performance test suites
- `docs/` – Architecture, threat model, data classification, cost model

---

## Getting Started

### Prerequisites

- Python 3.10+
- `pip` for dependency management

### Installation

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Testing

```bash
pytest
```

