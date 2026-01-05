# app/api/trades.py

from fastapi import APIRouter, Depends
from typing import List
from app.models.trade import Trade
from app.store.memory import TRADES
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/trades", response_model=List[Trade], tags=["Trades"])
def list_trades(user_id: str = Depends(get_current_user)):
    """
    Return executed trades for the authenticated user (in-memory).
    """
    return [t for t in TRADES if t.get("user_id") == user_id]
