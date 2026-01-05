# app/api/ws.py
from fastapi import APIRouter, WebSocket
from app.services.broadcaster import broadcaster

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await broadcaster.connect(ws)
    try:
        while True:
            # we expect clients to ping occasionally, but ignore receives
            await ws.receive_text()
    except Exception:
        pass
    finally:
        broadcaster.disconnect(ws)
