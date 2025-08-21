# Aegis-IMX Risk Engine

This project provides a minimal risk engine capable of running Value-at-Risk (VaR) computations via a FastAPI service.

## Features
- Parametric and Historical VaR calculations using Polars
- FastAPI endpoints for executing risk runs and fetching results
- In-memory caching of run results
- Basic unit tests with `pytest`

## API
- `POST /risk/run` with JSON body `{portfolio_id, as_of, method, positions?, returns?}`
  - `positions` required for `parametric` method
  - `returns` required for `historical` method
- `GET /risk/results/{run_id}` retrieves cached results

## Development
```bash
pip install -r requirements.txt  # if available
uvicorn risk_engine.api:app --reload
pytest
```
