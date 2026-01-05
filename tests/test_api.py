import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_market_order_flow():
    headers = {"x-api-key": "demo-key"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/api/v1/instruments", headers=headers)
        assert r.status_code == 200
        instruments = r.json()
        assert isinstance(instruments, list) and len(instruments) > 0

        payload = {
            "symbol": "RELIANCE",
            "order_type": "BUY",
            "order_style": "MARKET",
            "quantity": 1
        }
        r = await ac.post("/api/v1/orders", json=payload, headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert data["state"] == "EXECUTED"
        order_id = data["order_id"]

        r = await ac.get(f"/api/v1/orders/{order_id}", headers=headers)
        assert r.status_code == 200

        r = await ac.get("/api/v1/trades", headers=headers)
        assert r.status_code == 200
        trades = r.json()
        assert any(t["order_id"] == order_id for t in trades)

        r = await ac.get("/api/v1/portfolio", headers=headers)
        assert r.status_code == 200
        pf = r.json()
        assert pf.get("user_id") == "demo-user"
