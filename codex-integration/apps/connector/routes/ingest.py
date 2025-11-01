from fastapi import APIRouter
from pydantic import BaseModel
from apps.connector.services.router import route_event

router = APIRouter()

class CanonEvent(BaseModel):
	type: str
	source: str
	data: dict

@router.post("/")
async def ingest_event(event: CanonEvent):
	result = await route_event(event.dict())
	return {"status": "accepted", "id": result.get("id")}
