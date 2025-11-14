from fastapi import APIRouter, HTTPException
from app.models import CeremonyCreate, OathRecord
import uuid, datetime

router = APIRouter()
CEREMONIES = {}

@router.post("")
def schedule(payload: CeremonyCreate):
    cid = str(uuid.uuid4())
    CEREMONIES[cid] = {"id": cid, "status": "scheduled", **payload.dict()}
    return CEREMONIES[cid]

@router.post("/{ceremony_id}/start")
def start(ceremony_id: str):
    c = CEREMONIES.get(ceremony_id)
    if not c: raise HTTPException(404, "Ceremony not found")
    c["status"] = "active"
    return c

@router.post("/{ceremony_id}/oath")
def record_oath(ceremony_id: str, oath: OathRecord):
    c = CEREMONIES.get(ceremony_id)
    if not c: raise HTTPException(404, "Ceremony not found")
    c.setdefault("oaths", []).append(oath.dict())
    return {"ok": True, "count": len(c["oaths"])}

@router.post("/{ceremony_id}/close")
def close(ceremony_id: str):
    c = CEREMONIES.get(ceremony_id)
    if not c: raise HTTPException(404, "Ceremony not found")
    c["status"] = "archived"
    c["closed_at"] = datetime.datetime.utcnow().isoformat()
    return c
