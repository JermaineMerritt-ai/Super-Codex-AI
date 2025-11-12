# app/ws.py
from fastapi import APIRouter, WebSocket
from app.workflow import WORKFLOWS

ws_router = APIRouter()

clients = set()

@ws_router.websocket("/ws/ceremony")
async def ceremony(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # keep-alive or client pings
    except Exception:
        clients.remove(ws)

async def broadcast_event(event: dict):
    to_remove = []
    for c in clients:
        try:
            await c.send_json(event)
        except Exception:
            to_remove.append(c)
    for c in to_remove:
        clients.remove(c)