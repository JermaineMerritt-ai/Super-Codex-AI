# services/capsules.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
router = APIRouter()

class CapsuleCreate(BaseModel):
  id: str
  title: str
  sigil: str
  createdAt: str
  description: Optional[str] = None

CAPSULES = [
  {"id": "C-001", "title": "Omega Benediction", "sigil": "SIGIL-OMEGA-001", "createdAt": "2025-11-13T00:00:00Z"},
  {"id": "C-002", "title": "Final Eternal Charter", "sigil": "SIGIL-OMEGA-CHARTER-001", "createdAt": "2025-11-13T00:00:00Z"},
  {"id": "C-003", "title": "Final Eternal Charter Capsule", "sigil": "SIGIL-OMEGA-CHARTER-001", "createdAt": "2025-11-13T11:15:00Z", "description": "Supreme covenant capsule binding heirs, councils, and custodians under the radiant flame."}
]

@router.get("/api/capsules")
def list_capsules():
  return CAPSULES

@router.get("/api/capsules/{cid}")
def get_capsule(cid: str):
  return next((c for c in CAPSULES if c["id"] == cid), None)

@router.post("/api/capsules")
def create_capsule(capsule: CapsuleCreate):
  # Check if capsule with same ID already exists
  if any(c["id"] == capsule.id for c in CAPSULES):
    raise HTTPException(status_code=400, detail="Capsule with this ID already exists")
  
  # Convert to dict and add to CAPSULES
  new_capsule = capsule.dict()
  CAPSULES.append(new_capsule)
  return new_capsule