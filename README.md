# Aegis-IMX

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
- `tests/` – E2E, chaos, and performance tests
- `docs/` – Architecture, threat model, data classification, cost model

Refer to `docs/architecture.md` for the full system specification.
