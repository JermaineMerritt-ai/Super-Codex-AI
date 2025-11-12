# app/routes_workflow.py
from fastapi import APIRouter, HTTPException
from app.workflow import start_workflow, advance_workflow, WORKFLOWS, Phase

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/start")
def start(name: str, data: dict):
    return start_workflow(name, data)

@router.post("/{wid}/advance")
def advance(wid: str, phase: Phase, patch: dict | None = None):
    if wid not in WORKFLOWS:
        raise HTTPException(404, "Workflow not found")
    return advance_workflow(wid, phase, patch)

@router.get("/{wid}")
def get(wid: str):
    return WORKFLOWS.get(wid) or {}