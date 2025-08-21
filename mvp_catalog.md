# MVP Catalog

## Risk Engine MVP
- Parametric and Historical VaR calculations
- FastAPI interface for running risk and retrieving results
- Supports positions for parametric and returns data for historical VaR
- In-memory cache for run results
=======
This catalog enumerates Phase 0 vertical slices. Each slice includes deliverables across infrastructure, services, APIs, UI, tests, sample data, runbooks, and observability hooks.

## 1. Data Lake & Ingestion
- **Repo**: `datalake-ingestion`
- **Interfaces**: REST/GraphQL endpoints for data loading; S3-compatible object storage; Kafka topics for streaming ingestion.
- **Schemas**: Market data, reference data, positions, transactions stored in parquet with metadata catalog in Glue-compatible format.
- **Test Plan**:
  - Unit: schema validation and ETL transforms.
  - Integration: ingestion of sample market and trade files; contract tests for Kafka publishers.
  - UAT: end-to-end ingestion of daily market data drop.
- **Security Model**: Enforce PII minimization via field-level encryption; IAM roles with least privilege; SOC2-style access logs.
- **Integration Tests**: Validate Portfolio/Risk and Performance services can query normalized datasets.

## 2. Portfolio & Risk Core
- **Repo**: `portfolio-risk-core`
- **Interfaces**: gRPC service for risk calculations; REST endpoints for exposures and VaR; reads from Data Lake tables.
- **Schemas**: Position snapshot, exposure vectors, factor model coefficients, VaR results.
- **Test Plan**:
  - Unit: risk factor calculations, scenario shocks.
  - Integration: round-trip from Data Lake positions to VaR output.
  - UAT: compare VaR against known benchmarks.
- **Security Model**: Role-based access via JWT; encrypted temp files; audit logging of calculation requests.
- **Integration Tests**: Ensure risk outputs feed Performance and Reporting modules.

## 3. OMS/EMS Lite
- **Repo**: `oms-ems-lite`
- **Interfaces**: REST endpoints for order entry and allocation; WebSocket for execution updates; publishes events to Kafka.
- **Schemas**: Orders, executions, allocations in JSON with FIX tag mapping.
- **Test Plan**:
  - Unit: order validation, allocation logic.
  - Integration: simulated FIX/TWICE flows; Compliance pre-trade check stubs.
  - UAT: demo trade lifecycle through mock broker.
- **Security Model**: OAuth2 client credentials; signed FIX messages; full order/event audit trail.
- **Integration Tests**: Verify Compliance engine intercepts orders and Data Lake receives execution events.

## 4. Compliance Rules Engine
- **Repo**: `compliance-engine`
- **Interfaces**: gRPC/REST API for rule evaluation; consumes OMS events; writes results to audit log store.
- **Schemas**: Rule definitions, evaluation results, breach reports.
- **Test Plan**:
  - Unit: individual rule functions.
  - Integration: OMS pre- and post-trade checks using sample orders.
  - UAT: regulatory scenario walkthrough.
- **Security Model**: Signed rule deployments; immutable audit trail in Governance layer; PII redaction of client identifiers.
- **Integration Tests**: Confirm breach events propagate to Reporting and Governance logs.

## 5. Performance & Attribution
- **Repo**: `performance-attribution`
- **Interfaces**: REST API returning time-weighted returns and contribution tables; consumes Data Lake and Risk outputs.
- **Schemas**: Period returns, attribution by sector/factor, benchmark series.
- **Test Plan**:
  - Unit: return calculations and attribution factors.
  - Integration: tie-out against Data Lake positions and Risk exposures.
  - UAT: portfolio sample vs benchmark.
- **Security Model**: Signed result sets; anonymized portfolio identifiers; access logging.
- **Integration Tests**: Verify outputs feed Reporting dashboards.

## 6. Reporting & Client Portal
- **Repo**: `reporting-portal`
- **Interfaces**: GraphQL API for dashboards; React/Next.js web UI; reads Performance, Risk, and Compliance data.
- **Schemas**: Report definitions, widget configs, client entitlements.
- **Test Plan**:
  - Unit: UI component tests and API resolvers.
  - Integration: cross-service queries to Risk, Performance, Compliance.
  - UAT: client statement generation.
- **Security Model**: MFA-enabled auth; per-client data partitioning; content-security policy headers.
- **Integration Tests**: Full portal load with sample data; audit hook verification with Governance service.

## 7. Governance, Audit & Explainability
- **Repo**: `governance-audit`
- **Interfaces**: Append-only log API; policy engine for data retention; exposes audit search to Reporting.
- **Schemas**: Service logs, access events, explainability metadata.
- **Test Plan**:
  - Unit: log write/read, retention enforcement.
  - Integration: ingest logs from each service; query via Reporting.
  - UAT: SOC2 control walkthrough.
- **Security Model**: WORM storage; hashed log blocks; strict PII minimization policies.
- **Integration Tests**: Validate end-to-end audit trail from OMS order to Reporting view.
