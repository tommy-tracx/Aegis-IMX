# Aegis-IMX

Enterprise architecture and reference implementation for institutional investment management by NeuralQuantum.ai.

## Features
- Modular microservices: portfolio, risk, order management, compliance, and performance.
- Zero-trust security with OIDC, OPA, and mTLS service mesh.
- Event-driven integration via Kafka/Redpanda.
- Lakehouse data platform using Delta/Iceberg, Spark, and Flink.

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

## Getting Started
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the minimal portfolio service:
```bash
uvicorn portfolio_service.main:app --reload
```

## Testing
Execute unit tests:
```bash
pytest
```

## Documentation
Additional architectural and operational guides are available in the [docs](docs/README.md) directory.
