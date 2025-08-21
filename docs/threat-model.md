# Threat Model

## Assets
- Market data
- Trade orders
- Portfolio holdings
- User credentials

## Actors
- Internal users
- External clients
- Malicious attackers
- Rogue insiders

## Entry Points
- API Gateway
- Event bus
- Data ingestion endpoints

## Mitigations
- mTLS for all service-to-service traffic
- OIDC-authenticated JWTs
- OPA/Rego policies enforcing ABAC
- Web Application Firewall
- Encryption at rest and in transit
- Least privilege access
