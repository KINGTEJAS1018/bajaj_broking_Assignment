# app/services/limit_matcher.py
import asyncio
from app.store.memory import ORDERS
from app.services.execution_engine import execute_if_possible

RUN_INTERVAL_SECONDS = 2.0  # check every 2s

async def matcher_loop():
    print("[Background] Limit Order Matcher started...")
    while True:
        try:
            # Create a copy of items to avoid "dictionary changed size during iteration" error
            # This is a common bug in Python loops modifying dicts
            current_orders = list(ORDERS.items())
            
            for order_id, order in current_orders:
                if order["state"] == "PLACED" and order["order_style"] == "LIMIT":
                    # attempt execution (may return a trade)
                    # We now AWAIT the result
                    await execute_if_possible(order)
            
            await asyncio.sleep(RUN_INTERVAL_SECONDS)
        except Exception as e:
            print(f"Matcher error: {e}")
            await asyncio.sleep(RUN_INTERVAL_SECONDS)