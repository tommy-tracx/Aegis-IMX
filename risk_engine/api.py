"""FastAPI service exposing risk engine."""
from __future__ import annotations

from datetime import date
from typing import Optional

import polars as pl
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .engine import RiskEngine
from .models import PortfolioSnapshot

app = FastAPI(title="Risk Engine")
engine = RiskEngine()


class RunRequest(BaseModel):
    portfolio_id: str
    as_of: date
    method: str = "parametric"
    positions: Optional[list[dict]] = None  # list of {asset, value, factor1,...}
    returns: Optional[list[dict]] = None  # list of {"return": value}


class RunResponse(BaseModel):
    run_id: str


class ResultResponse(BaseModel):
    run_id: str
    results: dict


@app.post("/risk/run", response_model=RunResponse)
def run_risk(req: RunRequest) -> RunResponse:
    snapshot = None
    returns_df = None
    if req.positions is not None:
        snapshot = PortfolioSnapshot(pl.DataFrame(req.positions))
    if req.returns is not None:
        returns_df = pl.DataFrame(req.returns)
    try:
        run_id = engine.run_risk(snapshot, returns=returns_df, method=req.method)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RunResponse(run_id=run_id)


@app.get("/risk/results/{run_id}", response_model=ResultResponse)
def get_results(run_id: str) -> ResultResponse:
    try:
        res = engine.get_results(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="run_id not found") from exc
    return ResultResponse(run_id=run_id, results=res)
