# Aegis-IMX

## Portfolio Service

This project provides a minimal FastAPI implementation of a portfolio service.
It supports portfolio CRUD operations with role-based access control and basic
position aggregation.

### Setup

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest
```
=======
Enterprise architecture and reference implementation for institutional investment management.

## Repository Layout
- `infra/` – Terraform, Helm, GitHub Actions
- `gateway/` – API Gateway with OPA plugin
- `idp/` – OIDC provider
- `lake/` – Delta/Iceberg lakehouse
- `services/` – Core domain microservices
- `ui/` – Next.js/React front-end
- `mlops/` – Model registry and feature pipelines
- `shared/` – Libraries and schemas
- `tools/` – Orchestration utilities
- `tests/` – E2E, chaos, and performance tests
- `docs/` – Architecture, threat model, data classification, cost model
