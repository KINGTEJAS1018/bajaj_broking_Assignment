# app/api/orders.py

from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import get_current_user
from app.models.order import OrderRequest, OrderResponse, OrderState
from app.store import memory
from app.services.execution_engine import execute_if_possible, find_instrument
from uuid import uuid4
from datetime import datetime
from typing import Dict

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, tags=["Orders"])
async def place_order(payload: OrderRequest, user_id: str = Depends(get_current_user)):
    """
    Place an order. 
    Async handler to allow non-blocking execution of the matching engine.
    """
    # basic instrument existence check
    inst = find_instrument(payload.symbol)
    if not inst:
        raise HTTPException(status_code=404, detail="Instrument not found")

    order_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    order: Dict = {
        "order_id": order_id,
        "symbol": payload.symbol.upper(),
        "order_type": payload.order_type.value,
        "order_style": payload.order_style.value,
        "quantity": payload.quantity,
        "price": float(payload.price) if payload.price is not None else None,
        "state": OrderState.PLACED.value,
        "created_at": now,
        "executed_at": None,
        "user_id": user_id
    }

    # Save the order in memory
    memory.ORDERS[order_id] = order

    # Try executing immediately (MARKET or hitting LIMIT)
    try:
        # We now AWAIT the execution engine
        await execute_if_possible(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # return the current order state (it might have changed to EXECUTED inside execute_if_possible)
    return OrderResponse(**order)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse, tags=["Orders"])
def cancel_order(order_id: str, user_id: str = Depends(get_current_user)):
    order = memory.ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if order.get("state") in (OrderState.EXECUTED.value, OrderState.CANCELLED.value):
        raise HTTPException(status_code=400, detail="Cannot cancel executed or already cancelled order")
    
    order["state"] = OrderState.CANCELLED.value
    order["executed_at"] = None
    memory.ORDERS[order_id] = order
    return OrderResponse(**order)

@router.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order(order_id: str, user_id: str = Depends(get_current_user)):
    order = memory.ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return OrderResponse(**order)