from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from compliance import Policy, ComplianceEngine

policy = Policy.load("policies/policy_v1.yaml")
engine = ComplianceEngine(policy)

app = FastAPI(title="Compliance Engine")


class Order(BaseModel):
    symbol: str
    quantity: float
    issuer: str


class PortfolioState(BaseModel):
    positions: Dict[str, float]
    restricted_list: List[str] = []
    issuer_limits: Dict[str, float] = {}
    cash: float | None = None


class Fill(BaseModel):
    symbol: str
    quantity: float
    side: str


class PreTradeRequest(BaseModel):
    order: Order
    portfolio_state: PortfolioState


class PostTradeRequest(BaseModel):
    fills: List[Fill]
    portfolio_state: PortfolioState


@app.post("/compliance/pretrade")
def pre_trade(req: PreTradeRequest):
    passed, eval_id = engine.pre_trade(req.order.dict(), req.portfolio_state.dict())
    return {"passed": passed, "eval_id": eval_id}


@app.post("/compliance/posttrade")
def post_trade(req: PostTradeRequest):
    fills = [f.dict() for f in req.fills]
    passed, eval_id = engine.post_trade(fills, req.portfolio_state.dict())
    return {"passed": passed, "eval_id": eval_id}


@app.get("/compliance/explanations/{eval_id}")
def explanations(eval_id: str):
    return engine.get_explanation(eval_id)


__all__ = ["app"]
