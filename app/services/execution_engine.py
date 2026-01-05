# app/services/execution_engine.py

import asyncio
from app.services.broadcaster import broadcaster
from app.store.memory import INSTRUMENTS, TRADES, PORTFOLIO
from datetime import datetime
from uuid import uuid4
from typing import Optional

# Global lock to prevent race conditions during order execution
ENGINE_LOCK = asyncio.Lock()

def find_instrument(symbol: str) -> Optional[dict]:
    symbol_upper = symbol.upper()
    for inst in INSTRUMENTS:
        if inst["symbol"].upper() == symbol_upper:
            return inst
    return None

async def execute_if_possible(order: dict) -> Optional[dict]:
    """
    Async execution engine.
    Uses a Lock to ensure thread-safety when updating Portfolio and Trades.
    """
    inst = find_instrument(order["symbol"])
    if not inst:
        raise ValueError("Instrument not found")

    ltp = inst["last_traded_price"]
    executed_price = None

    # MARKET -> execute immediately at LTP
    if order["order_style"] == "MARKET":
        executed_price = ltp

    # LIMIT -> execute only if price condition met
    elif order["order_style"] == "LIMIT":
        if order["order_type"] == "BUY" and order["price"] >= ltp:
            executed_price = order["price"]
        if order["order_type"] == "SELL" and order["price"] <= ltp:
            executed_price = order["price"]

    if executed_price is None:
        return None

    # CRITICAL SECTION: Lock the state before modifying global dictionaries
    async with ENGINE_LOCK:
        # Double-check state in case it changed while waiting for lock
        if order["state"] == "EXECUTED":
            return None

        # Mark order executed
        order["state"] = "EXECUTED"
        order["executed_at"] = datetime.utcnow().isoformat()
        
        user_id = order.get("user_id", "demo-user")

        # Create trade record
        trade = {
            "trade_id": str(uuid4()),
            "order_id": order["order_id"],
            "symbol": order["symbol"],
            "quantity": order["quantity"],
            "price": float(executed_price),
            "side": order["order_type"],
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id
        }
        TRADES.append(trade)

        # Update portfolio
        user_portfolio = PORTFOLIO.setdefault(user_id, {})
        holding = user_portfolio.get(order["symbol"], {"quantity": 0, "avg_price": 0.0})

        if order["order_type"] == "BUY":
            prev_qty = holding["quantity"]
            prev_avg = holding["avg_price"]
            new_qty = prev_qty + order["quantity"]
            
            if new_qty == 0:
                new_avg = 0.0
            else:
                total_cost = (prev_qty * prev_avg) + (order["quantity"] * executed_price)
                new_avg = total_cost / new_qty
            
            holding["quantity"] = new_qty
            holding["avg_price"] = new_avg
        
        else:  # SELL
            holding["quantity"] = holding.get("quantity", 0) - order["quantity"]
            # avg_price remains unchanged on sell

        user_portfolio[order["symbol"]] = holding
        PORTFOLIO[user_id] = user_portfolio

    # Broadcast trade update (Safe to do outside lock, but needs await)
    await broadcaster.broadcast({"type": "trade", "trade": trade})

    return trade