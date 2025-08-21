# Aegis-IMX Compliance Engine

A lightweight compliance engine supporting pre-trade and post-trade rule evaluation with policy versioning and audit explanations.

## Features
- Rules defined via a simple DSL evaluated against trade context.
- Policy versioning with signatures and approvals.
- FastAPI endpoints for pre-trade, post-trade, and explanation retrieval.
- Deterministic evaluation with human-readable explanations.

## API
- `POST /compliance/pretrade` – evaluate an order against pre-trade rules.
- `POST /compliance/posttrade` – evaluate fills against post-trade rules.
- `GET /compliance/explanations/{eval_id}` – retrieve evaluation explanations.

## Development
Install dependencies and run tests:

```bash
pip install -r requirements.txt
pytest
```
