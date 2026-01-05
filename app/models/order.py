# app/models/order.py

from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderRequest(BaseModel):
    symbol: str
    order_type: OrderType
    order_style: OrderStyle
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    price: Optional[float] = None

    @validator("price")
    def price_required_for_limit(cls, v, values):
        if values.get("order_style") == OrderStyle.LIMIT and v is None:
            raise ValueError("price is required for LIMIT orders")
        return v

class OrderResponse(BaseModel):
    order_id: str
    symbol: str
    order_type: OrderType
    order_style: OrderStyle
    quantity: int
    price: Optional[float] = None
    state: str
    created_at: str
    executed_at: Optional[str] = None


class OrderState(str, Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
