# app/store/memory.py

from typing import Dict, List

# Seeded list of instruments (acts like a small "table")
INSTRUMENTS = [
    {
        "symbol": "RELIANCE",
        "exchange": "NSE",
        "instrument_type": "EQ",
        "last_traded_price": 2500.00
    },
    {
        "symbol": "TCS",
        "exchange": "NSE",
        "instrument_type": "EQ",
        "last_traded_price": 3800.00
    },
    {
        "symbol": "INFY",
        "exchange": "NSE",
        "instrument_type": "EQ",
        "last_traded_price": 1500.50
    }
]

# Orders stored as order_id -> order dict
ORDERS: Dict[str, dict] = {}

# Trades as a list of trade dicts
TRADES: List[dict] = []

# Portfolio per user_id: { user_id: { symbol: { quantity, avg_price } } }
PORTFOLIO: Dict[str, Dict[str, dict]] = {}
