from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .models import (
    Order,
    OrderSide,
    OrderStatus,
    ChildOrder,
    Allocation,
)
from .compliance import ComplianceEngine
from .events import publish

app = FastAPI(title="OMS/EMS Lite")

orders: dict[int, Order] = {}
order_counter = 1
child_counter = 1

compliance = ComplianceEngine()


class OrderCreateRequest(BaseModel):
    symbol: str
    side: OrderSide
    quantity: int
    price: float


class RouteRequest(BaseModel):
    venue: str
    quantity: int


class AllocationRequest(BaseModel):
    allocations: List[Allocation]


@app.post("/orders", response_model=Order)
def create_order(req: OrderCreateRequest) -> Order:
    global order_counter
    order = Order(id=order_counter, **req.model_dump())
    try:
        compliance.validate(order)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    orders[order.id] = order
    publish(order, "order_created.v1")
    publish(order, "pretrade_passed.v1")
    order_counter += 1
    return order


@app.post("/orders/{order_id}/route", response_model=Order)
def route_order(order_id: int, req: RouteRequest) -> Order:
    global child_counter
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    child = ChildOrder(
        id=child_counter, venue=req.venue, quantity=req.quantity, filled_quantity=req.quantity
    )
    child_counter += 1
    order.child_orders.append(child)
    order.filled_quantity += child.filled_quantity
    order.status = (
        OrderStatus.FILLED if order.filled_quantity >= order.quantity else OrderStatus.PARTIALLY_FILLED
    )
    publish(
        order,
        "execution_fill.v1",
        {"child_id": str(child.id), "quantity": str(child.filled_quantity)},
    )
    return order


@app.post("/orders/{order_id}/allocate", response_model=Order)
def allocate_order(order_id: int, req: AllocationRequest) -> Order:
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    total_alloc = sum(a.quantity for a in req.allocations)
    if total_alloc != order.filled_quantity:
        raise HTTPException(
            status_code=400, detail="Allocation quantities must equal filled quantity"
        )
    order.allocations = req.allocations
    return order
