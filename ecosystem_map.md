# Ecosystem Map

- `risk_engine/`: core risk calculations and API service
- `tests/`: unit tests covering parametric and historical VaR
- `ui/`: Flutter-based cross-platform client
- Documentation files: `README.md`, `mvp_catalog.md`, `component_map.md`
## Overview
Aegis-IMX is a modular investment management platform composed of seven core services. Each service is delivered as a vertical slice with its own infrastructure, service layer, APIs, UI, tests, data samples, runbooks, and observability hooks.

## Services and Dependencies
- **Data Lake & Ingestion**: Centralized storage for market, reference, position, and transaction data. Feeds downstream analytics and transactional systems.
- **Portfolio & Risk Core**: Calculates exposures, factor risks, and value-at-risk by reading normalized data from the Data Lake.
- **OMS/EMS Lite**: Manages orders and allocations, publishing execution events to the Data Lake and invoking Compliance checks.
- **Compliance Rules Engine**: Validates pre- and post-trade constraints. Subscribes to OMS events and writes audit results to Governance logs.
- **Performance & Attribution**: Generates performance metrics using Data Lake positions and transactions; outputs attribution reports to Reporting.
- **Reporting & Client Portal**: Presents dashboards and statements. Consumes outputs from Performance and Data Lake; interfaces with Governance for audit trails.
- **Governance, Audit & Explainability**: Cross-cutting layer providing SOC2-style logging, PII minimization enforcement, and explainability metadata for all services.

## Integration Points
- Risk and Performance services query standardized datasets from the Data Lake.
- OMS triggers Compliance checks before order submission and records decisions.
- Reporting aggregates outputs from Risk, Performance, and Compliance.
- Governance ingests logs from every service for unified audit and explainability.
