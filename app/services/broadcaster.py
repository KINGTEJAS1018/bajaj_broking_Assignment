# app/services/broadcaster.py
import asyncio
from typing import Set
from fastapi import WebSocket

class Broadcaster:
    def __init__(self):
        self.clients: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)

    async def broadcast(self, message: dict):
        dead = []
        for ws in list(self.clients):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for d in dead:
            self.disconnect(d)

broadcaster = Broadcaster()
