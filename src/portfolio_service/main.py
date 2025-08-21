import logging
from typing import List, Sequence

from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .db import Base, engine, get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio Service")

ALLOWED_ROLES = {"PM", "Risk", "Ops", "Compliance", "Client"}


def get_role(x_role: str = Header(...)) -> str:
    """Validate and return the caller's role from headers."""
    if x_role not in ALLOWED_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")
    return x_role


def require_roles(roles: Sequence[str]):
    """Dependency factory enforcing role-based access."""

    def checker(role: str = Depends(get_role)) -> str:
        if role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )
        return role

    return checker


@app.post(
    "/portfolios",
    response_model=schemas.PortfolioRead,
    dependencies=[Depends(require_roles({"PM", "Ops", "Compliance"}))],
)
def create_portfolio(
    portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)
):
    """Create a new portfolio with optional positions."""
    logger.info("Creating portfolio %s", portfolio.name)
    db_portfolio = models.Portfolio(name=portfolio.name)
    for pos in portfolio.positions:
        db_portfolio.positions.append(
            models.Position(
                instrument=pos.instrument, quantity=pos.quantity, sector=pos.sector
            )
        )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@app.get(
    "/portfolios/{portfolio_id}",
    response_model=schemas.PortfolioRead,
    dependencies=[Depends(require_roles(ALLOWED_ROLES))],
)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.get(models.Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return portfolio


@app.put(
    "/portfolios/{portfolio_id}",
    response_model=schemas.PortfolioRead,
    dependencies=[Depends(require_roles({"PM", "Ops", "Compliance"}))],
)
def update_portfolio(
    portfolio_id: int, data: schemas.PortfolioBase, db: Session = Depends(get_db)
):
    portfolio = db.get(models.Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    portfolio.name = data.name
    db.commit()
    db.refresh(portfolio)
    return portfolio


@app.delete(
    "/portfolios/{portfolio_id}",
    dependencies=[Depends(require_roles({"Ops"}))],
)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.get(models.Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(portfolio)
    db.commit()
    return {"status": "deleted"}


@app.get(
    "/portfolios/{portfolio_id}/positions",
    dependencies=[Depends(require_roles(ALLOWED_ROLES))],
)
def aggregated_positions(portfolio_id: int, db: Session = Depends(get_db)) -> List[dict]:
    """Return aggregated positions for a portfolio grouped by instrument."""
    exists = db.get(models.Portfolio, portfolio_id)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    rows = (
        db.query(
            models.Position.instrument,
            func.sum(models.Position.quantity).label("quantity"),
        )
        .filter(models.Position.portfolio_id == portfolio_id)
        .group_by(models.Position.instrument)
        .all()
    )
    return [{"instrument": r.instrument, "quantity": r.quantity} for r in rows]
