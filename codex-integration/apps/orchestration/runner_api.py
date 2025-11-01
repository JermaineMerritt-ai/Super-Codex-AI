from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .flows_store import get_flow
from .runner import run_flow

exec_router = APIRouter(prefix="/runs", tags=["runs"])

class RunRequest(BaseModel):
    flow_id: str
    event: dict
    dry_run: bool = True

@exec_router.post("")
async def start_run(req: RunRequest):
    flow = get_flow(req.flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    ctx = await run_flow(flow, req.event, req.dry_run)
    return ctx
