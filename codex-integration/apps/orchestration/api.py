from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/workflows", tags=["workflows"])

class Capsule(BaseModel):
    id: str
    version: int
    yaml: str

DB = {"capsules": {}}

@router.get("")
def list_capsules():
    return list(DB["capsules"].values())

@router.post("")
def save_capsule(capsule: Capsule):
    DB["capsules"][capsule.id] = capsule.model_dump()
    return {"status": "saved", "id": capsule.id, "version": capsule.version}

@router.post("/{id}/publish")
def publish_capsule(id: str):
    cap = DB["capsules"].get(id)
    cap["published"] = True
    cap["sealed_id"] = f"{id}-v{cap['version']}"
    return {"status": "published", "sealed_id": cap["sealed_id"]}

runs = APIRouter(prefix="/runs", tags=["runs"])

class RunRequest(BaseModel):
    capsule_id: str
    event: dict
    dry_run: bool = True

@runs.post("")
async def start_run(req: RunRequest):
    run_id = str(uuid.uuid4())
    # invoke engine.run with dry_run flag (placeholder)
    return {"run_id": run_id, "status": "started", "dry_run": req.dry_run}
