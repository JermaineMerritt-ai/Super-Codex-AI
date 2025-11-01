from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

flows = {}
node_types = [
    {"type": "trigger", "schema": {"event": {"type": "string"}}},
    {"type": "action", "schema": {"action": {"type": "string"}, "params": {"type": "object"}}},
    {"type": "condition", "schema": {"expr": {"type": "string"}}},
    {"type": "replay", "schema": {"strategy": {"type": "string"}}},
    {"type": "recognition", "schema": {"role": {"type": "string"}, "message": {"type": "string"}}},
]

router = APIRouter(prefix="/flows", tags=["flows"])

class CapsuleFlow(BaseModel):
    capsule: dict
    nodes: list
    edges: list
    guards: dict | None = None
    replay: dict | None = None

@router.get("")
def list_flows():
    return list(flows.values())

@router.post("")
def save_flow(flow: CapsuleFlow):
    fid = flow.capsule["id"]
    flows[fid] = flow.model_dump()
    return {"status": "saved", "id": fid, "version": flow.capsule.get("version", 1)}

@router.post("/{fid}/publish")
def publish_flow(fid: str):
    if fid not in flows:
        raise HTTPException(status_code=404, detail="Flow not found")
    flows[fid]["capsule"]["status"] = "sealed"
    flows[fid]["capsule"]["sealed_id"] = f"{fid}-v{flows[fid]['capsule']['version']}"
    return {"status": "sealed", "sealed_id": flows[fid]["capsule"]["sealed_id"]}

@router.get("/nodes")
def list_node_types():
    return node_types
