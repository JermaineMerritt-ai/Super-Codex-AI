from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/replay", tags=["replay"])

class ReplayItem(BaseModel):
  run_id: str
  flow_id: str
  payload: dict

REPLAY = []

@router.get("")
def list_replay():
    return REPLAY

@router.post("")
def enqueue(item: ReplayItem):
    REPLAY.append({
        "id": str(uuid.uuid4()),
        "run_id": item.run_id,
        "flow_id": item.flow_id,
        "status": "pending",
        "attempts": 0,
        "payload": item.payload
    })
    return {"status": "queued"}

@router.post("/{id}/redrive")
def redrive(id: str):
    # find item, run through runner; update attempts/status (placeholder)
    return {"status": "replayed", "id": id}
