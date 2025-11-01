from fastapi import APIRouter, Request, Header
from apps.connector.services.normalizer import normalize_payload
from apps.connector.services.router import route_event
from apps.connector.services.retries import retryable

router = APIRouter()

@router.post("/{source}")
@retryable
async def accept_webhook(source: str, request: Request, x_event: str | None = Header(default=None)):
	payload = await request.json()
	canon_event = normalize_payload(source, x_event, payload)
	result = await route_event(canon_event)
	return {"status": "accepted", "event": canon_event["type"], "id": result.get("id")}
