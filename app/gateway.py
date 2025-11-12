# app/gateway.py
import os
import httpx
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/axiom", tags=["AXIOM"])

AXIOM_BASE = os.getenv("AXIOM_BASE", "http://localhost:5010")  # dev default

class AxiomRequest(BaseModel):
    command: str
    payload: dict | None = None

@router.post("/execute")
async def execute(req: AxiomRequest):
    """
    Unified AXIOM proxy endpoint - routes all ceremonial commands through single interface.
    Frontend calls this endpoint only, never calls Flask directly.
    
    Supported commands:
    - health: Check AXIOM system status
    - reason: Ceremonial reasoning operations  
    - grant: Honor granting operations
    - ceremonies: List ceremonial records
    - broadcast: Broadcast messages to realms
    """
    command = req.command.lower()
    payload = req.payload or {}
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Route command to appropriate AXIOM endpoint
            if command == "health":
                r = await client.get(f"{AXIOM_BASE}/health")
            elif command == "reason":
                r = await client.post(f"{AXIOM_BASE}/reason", json=payload)
            elif command == "grant": 
                r = await client.post(f"{AXIOM_BASE}/grant", json=payload)
            elif command == "ceremonies":
                r = await client.get(f"{AXIOM_BASE}/ceremonies")
            elif command == "broadcast":
                # If AXIOM has broadcast endpoint, route there; otherwise handle locally
                r = await client.post(f"{AXIOM_BASE}/broadcast", json=payload)
            else:
                # Generic execute fallback - pass through to AXIOM if it has execute endpoint
                r = await client.post(f"{AXIOM_BASE}/execute", json=req.dict())
                
        r.raise_for_status()
        return {
            "status": "success",
            "command": command,
            "timestamp": datetime.datetime.now().isoformat(),
            "result": r.json()
        }
    except httpx.HTTPError as e:
        detail = getattr(e.response, "text", str(e)) if hasattr(e, 'response') else str(e)
        raise HTTPException(
            status_code=502, 
            detail=f"AXIOM {command} operation failed: {detail}"
        )

@router.get("/health")
async def health():
    """Check AXIOM system health via proxy"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{AXIOM_BASE}/health")
        r.raise_for_status()
        return {"status": "healthy", "axiom_base": AXIOM_BASE, "response": r.json()}
    except httpx.HTTPError as e:
        detail = getattr(e.response, "text", str(e))
        raise HTTPException(status_code=502, detail=f"Axiom health check failed: {detail}")

@router.post("/reason")
async def reason(req: dict):
    """Proxy ceremonial reasoning requests"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{AXIOM_BASE}/reason", json=req)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        detail = getattr(e.response, "text", str(e))
        raise HTTPException(status_code=502, detail=f"Axiom reasoning error: {detail}")

@router.post("/grant")
async def grant(req: dict):
    """Proxy honor granting requests"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{AXIOM_BASE}/grant", json=req)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        detail = getattr(e.response, "text", str(e))
        raise HTTPException(status_code=502, detail=f"Axiom grant error: {detail}")

@router.get("/ceremonies")
async def ceremonies():
    """Get ceremonial records via proxy"""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{AXIOM_BASE}/ceremonies")
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        detail = getattr(e.response, "text", str(e))
        raise HTTPException(status_code=502, detail=f"Axiom ceremonies error: {detail}")