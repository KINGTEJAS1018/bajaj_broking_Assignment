# app/models/trade.py

from pydantic import BaseModel
from typing import Optional

class Trade(BaseModel):
    trade_id: str
    order_id: str
    symbol: str
    quantity: int
    price: float
    side: str
    timestamp: str
