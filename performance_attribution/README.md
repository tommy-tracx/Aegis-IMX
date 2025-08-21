# Performance & Attribution Service

FastAPI service providing portfolio performance metrics and attribution results.

## Endpoints

- `POST /perf/run` – trigger a performance calculation run.
- `GET /perf/results/{run_id}` – retrieve results for a given run.

## Development

```bash
pip install -r requirements.txt
uvicorn performance_attribution.api:create_app --reload
```

## Testing

```bash
PYTHONPATH=/workspace/Aegis-IMX pytest performance_attribution/tests
```
