# app/workflow.py
from enum import Enum
from typing import Any
from pydantic import BaseModel
import uuid, time

class Phase(str, Enum):
    INIT="INIT"; DISPATCH="DISPATCH"; COMPLETE="COMPLETE"; ERROR="ERROR"

class WorkflowState(BaseModel):
    id: str
    name: str
    phase: Phase
    data: dict[str, Any]
    created_at: float
    updated_at: float

WORKFLOWS: dict[str, WorkflowState] = {}

def start_workflow(name: str, data: dict) -> WorkflowState:
    wid = str(uuid.uuid4())
    ws = WorkflowState(id=wid, name=name, phase=Phase.INIT, data=data, created_at=time.time(), updated_at=time.time())
    WORKFLOWS[wid] = ws
    return ws

def advance_workflow(wid: str, new_phase: Phase, patch: dict | None = None) -> WorkflowState:
    ws = WORKFLOWS[wid]
    ws.phase = new_phase
    if patch: ws.data.update(patch)
    ws.updated_at = time.time()
    WORKFLOWS[wid] = ws
    return ws