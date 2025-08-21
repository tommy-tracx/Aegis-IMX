# Development Queue

Priority = (Market Value × 0.4) + (Technical Feasibility × 0.3) + (Time-to-Market × 0.2) + (Strategic Importance × 0.1)

| Rank | Slice                         | MV | TF | TTM | SI | Priority |
|------|------------------------------|----|----|-----|----|----------|
| 1    | Data Lake & Ingestion        | 5  | 4  | 3   | 5  | 4.3      |
| 2    | Portfolio & Risk Core        | 5  | 3  | 2   | 5  | 3.8      |
| 3    | OMS/EMS Lite                 | 4  | 3  | 3   | 4  | 3.5      |
| 4    | Reporting & Client Portal    | 4  | 3  | 3   | 3  | 3.4      |
| 5    | Compliance Rules Engine      | 4  | 2  | 2   | 4  | 3.0      |
| 6    | Performance & Attribution    | 3  | 3  | 2   | 4  | 2.9      |
| 7    | Governance, Audit & Explainability | 3 | 2 | 1 | 5 | 2.5 |

## Task Assignments
### 1. Data Lake & Ingestion
- @AI: Build ML-driven schema validation for incoming files.
- @Backend: Implement ingestion APIs and Kafka publishers.
- @Frontend: Develop admin UI for ingestion monitoring.

### 2. Portfolio & Risk Core
- @AI: Implement factor model and VaR algorithms.
- @Backend: Expose risk calculation gRPC/REST services.
- @Frontend: Create dashboards for exposures and VaR.

### 3. OMS/EMS Lite
- @AI: Provide smart order routing stub.
- @Backend: Build order management REST/WebSocket services.
- @Frontend: Implement order entry and blotter UI.

### 4. Reporting & Client Portal
- @AI: Personalization model for client dashboards.
- @Backend: GraphQL resolvers integrating Risk, Performance, Compliance.
- @Frontend: React/Next.js portal with MFA login.

### 5. Compliance Rules Engine
- @AI: Rule-learning suggestions from historical breaches.
- @Backend: gRPC/REST rule evaluation service.
- @Frontend: Rule configuration UI.

### 6. Performance & Attribution
- @AI: Attribution factor analysis models.
- @Backend: REST APIs for return calculations.
- @Frontend: Visualization components for attribution reports.

### 7. Governance, Audit & Explainability
- @AI: Explainability metadata extractor.
- @Backend: Append-only log API and retention policies.
- @Frontend: Audit search interface.

