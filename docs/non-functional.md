# Non-Functional Requirements

## Scalability SLOs
- Throughput ≥ 10k TPS
- Latency p95 ≤ 100ms
- Latency p99 ≤ 200ms

## High Availability / Disaster Recovery
- RPO ≤ 5 minutes
- RTO ≤ 30 minutes
- Multi-AZ deployment

## Security
- mTLS for all service-to-service traffic
- JWT/OIDC authentication
- Fine-grained ABAC with OPA/Rego
- KMS envelope encryption for secrets and data at rest
