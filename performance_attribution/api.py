"""FastAPI app exposing performance endpoints."""

from fastapi import FastAPI, HTTPException

from .models import PerformanceResult, PerformanceRunRequest, PerformanceRunResponse
from .service import get_run, run_performance


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(title="Performance & Attribution")

    @app.post("/perf/run", response_model=PerformanceRunResponse)
    def perf_run(payload: PerformanceRunRequest) -> PerformanceRunResponse:
        result, run_id = run_performance(payload)
        return PerformanceRunResponse(run_id=run_id)

    @app.get("/perf/results/{run_id}", response_model=PerformanceResult)
    def perf_results(run_id: str) -> PerformanceResult:
        try:
            return get_run(run_id)
        except KeyError as exc:  # pragma: no cover - defensive
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app
