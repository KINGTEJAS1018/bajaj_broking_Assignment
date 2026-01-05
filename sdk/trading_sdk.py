# sdk/trading_sdk.py

import requests
from typing import Dict, Any, List

class TradingSDK:
    """
    Python SDK for Bajaj Broking Trading API
    """

    def __init__(self, base_url: str, api_key: str | None = None):
        """
        base_url example: http://127.0.0.1:8000
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key} if api_key else {}

    # -------- Instruments --------
    def get_instruments(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/api/v1/instruments", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_instrument(self, symbol: str) -> Dict[str, Any]:
        resp = requests.get(f"{self.base_url}/api/v1/instruments/{symbol}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    # -------- Orders --------
    def place_order(
        self,
        symbol: str,
        order_type: str,
        order_style: str,
        quantity: int,
        price: float | None = None
    ) -> Dict[str, Any]:
        payload = {     
            "symbol": symbol,
            "order_type": order_type,
            "order_style": order_style,
            "quantity": quantity
        }
        if price is not None:
            payload["price"] = price

        resp = requests.post(f"{self.base_url}/api/v1/orders", json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        resp = requests.get(f"{self.base_url}/api/v1/orders/{order_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    # -------- Trades --------
    def get_trades(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/api/v1/trades", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    # -------- Portfolio --------
    def get_portfolio(self, user_id: str = "demo-user") -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/api/v1/portfolio",
            params={"user_id": user_id},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()
