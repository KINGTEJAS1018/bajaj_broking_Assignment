# app/api/portfolio.py

from fastapi import APIRouter, Depends
from app.models.portfolio import PortfolioResponse, Holding
from app.store.memory import PORTFOLIO, INSTRUMENTS
from app.services.execution_engine import find_instrument
from app.core.auth import get_current_user

router = APIRouter()   # 🔥 REQUIRED — DO NOT REMOVE

@router.get(
    "/portfolio",
    response_model=PortfolioResponse,
    tags=["Portfolio"]
)
def get_portfolio(user_id: str = Depends(get_current_user)):
    """
    Get portfolio holdings for a user (default: demo-user)
    """
    user_portfolio = PORTFOLIO.get(user_id, {})
    holdings = []

    for symbol, data in user_portfolio.items():
        qty = int(data.get("quantity", 0))
        avg = float(data.get("avg_price", 0.0))
        # compute current value using instrument LTP if available
        inst = find_instrument(symbol)
        ltp = inst["last_traded_price"] if inst else 0.0
        current_value = qty * ltp
        holdings.append(
            Holding(
                symbol=symbol,
                quantity=qty,
                avg_price=avg,
                current_value=current_value
            )
        )

    return PortfolioResponse(
        user_id=user_id,
        holdings=holdings
    )
