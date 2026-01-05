# app/models/portfolio.py

from pydantic import BaseModel
from typing import List

class Holding(BaseModel):
    symbol: str
    quantity: int
    avg_price: float
    current_value: float


class PortfolioResponse(BaseModel):
    user_id: str
    holdings: List[Holding]
