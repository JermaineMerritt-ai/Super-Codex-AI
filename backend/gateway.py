# backend/gateway.py
import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/axiom", tags=["AXIOM-FLAME"])

# Use localhost for development, Docker service name for production
AXIOM_BASE = "http://127.0.0.1:8087"  # Local development
# AXIOM_BASE = "http://axiom-flame:5000"  # Docker production

class AxiomRequest(BaseModel):
    command: str
    payload: dict | None = None

class AxiomResponse(BaseModel):
    status: str
    data: dict | None = None
    error: str | None = None

class CeremonialRequest(BaseModel):
    actor: str = "Custodian"
    realm: str = "Planetary:Jackson-NC"
    capsule: str = "Crown Invocation"
    intent: str = "Ceremony.Dispatch"
    seal: str = "Eternal"
    reasoning: str = ""

@router.post("/execute", response_model=AxiomResponse)
async def execute(req: AxiomRequest):
    """Execute generic AXIOM FLAME command"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{AXIOM_BASE}/api/{req.command}", json=req.payload or {})
        
        if response.status_code >= 400:
            logger.error(f"AXIOM FLAME error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        return AxiomResponse(status="ok", data=data)
        
    except httpx.ConnectError as e:
        logger.error(f"AXIOM FLAME connection error: {e}")
        raise HTTPException(status_code=502, detail=f"AXIOM FLAME service unavailable: {e}")
    except httpx.TimeoutException:
        logger.error("AXIOM FLAME request timeout")
        raise HTTPException(status_code=504, detail="AXIOM FLAME request timeout")
    except httpx.RequestError as e:
        logger.error(f"AXIOM FLAME request error: {e}")
        raise HTTPException(status_code=502, detail=f"Gateway connection error: {e}")
    except Exception as e:
        logger.error(f"Gateway internal error: {e}")
        raise HTTPException(status_code=500, detail=f"Gateway internal error: {e}")

@router.post("/reason", response_model=AxiomResponse)
async def ceremonial_reason(req: CeremonialRequest):
    """Execute ceremonial reasoning via AXIOM FLAME"""
    try:
        payload = {
            "actor": req.actor,
            "realm": req.realm,
            "capsule": req.capsule,
            "intent": req.intent,
            "seal": req.seal,
            "reasoning": req.reasoning
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{AXIOM_BASE}/api/reason", json=payload)
        
        if response.status_code >= 400:
            logger.error(f"AXIOM FLAME reasoning error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        return AxiomResponse(status="reasoning_complete", data=data)
        
    except httpx.ConnectError as e:
        logger.error(f"AXIOM FLAME connection error: {e}")
        raise HTTPException(status_code=502, detail=f"AXIOM FLAME service unavailable: {e}")
    except Exception as e:
        logger.error(f"Ceremonial reasoning error: {e}")
        raise HTTPException(status_code=500, detail=f"Ceremonial reasoning error: {e}")

@router.get("/replay/{dispatch_id}", response_model=AxiomResponse)
async def replay_ceremony(dispatch_id: str):
    """Replay a ceremonial dispatch"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{AXIOM_BASE}/api/replay/{dispatch_id}")
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        return AxiomResponse(status="replay_complete", data=data)
        
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"AXIOM FLAME service unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Replay error: {e}")

@router.get("/audit/{dispatch_id}", response_model=AxiomResponse)
async def audit_ceremony(dispatch_id: str):
    """Audit a ceremonial dispatch"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{AXIOM_BASE}/api/audit/{dispatch_id}")
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        return AxiomResponse(status="audit_complete", data=data)
        
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"AXIOM FLAME service unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit error: {e}")

@router.get("/ledger", response_model=AxiomResponse)
async def list_ledger():
    """List all ceremonial ledger entries"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{AXIOM_BASE}/api/ledger")
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        return AxiomResponse(status="ledger_retrieved", data=data)
        
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"AXIOM FLAME service unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ledger retrieval error: {e}")

@router.get("/health")
async def gateway_health():
    """Check gateway and AXIOM FLAME health"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{AXIOM_BASE}/health")
        
        axiom_healthy = response.status_code == 200
        
        return {
            "gateway_status": "healthy",
            "axiom_flame_status": "healthy" if axiom_healthy else "unhealthy",
            "axiom_flame_url": AXIOM_BASE,
            "connection": "ok" if axiom_healthy else "failed"
        }
        
    except Exception as e:
        return {
            "gateway_status": "healthy",
            "axiom_flame_status": "unavailable",
            "axiom_flame_url": AXIOM_BASE,
            "connection": "failed",
            "error": str(e)
        }