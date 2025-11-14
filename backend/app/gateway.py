from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/api/gateway", tags=["gateway"])

logger = logging.getLogger(__name__)

class GatewayRequest(BaseModel):
    endpoint: str
    method: str = "GET"
    payload: Optional[dict] = None
    headers: Optional[dict] = None

class GatewayResponse(BaseModel):
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None
    timestamp: str

@router.post("/invoke")
async def invoke_gateway(request: GatewayRequest):
    """Universal gateway for invoking Codex services"""
    try:
        timestamp = datetime.utcnow().isoformat()
        
        # Route to appropriate service based on endpoint
        if request.endpoint.startswith("/capsule"):
            return await route_to_capsule_service(request, timestamp)
        elif request.endpoint.startswith("/ceremony"):
            return await route_to_ceremony_service(request, timestamp)
        elif request.endpoint.startswith("/dominion"):
            return await route_to_dominion_service(request, timestamp)
        elif request.endpoint.startswith("/axiom"):
            return await route_to_axiom_service(request, timestamp)
        else:
            raise HTTPException(status_code=404, detail=f"Unknown endpoint: {request.endpoint}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Gateway error: {e}")
        raise HTTPException(status_code=500, detail="Gateway processing failed")

async def route_to_capsule_service(request: GatewayRequest, timestamp: str):
    """Route requests to capsule services"""
    try:
        # Simulate capsule service routing
        if "/create" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"capsule_id": f"cap_{timestamp}", "message": "Capsule creation initiated"},
                timestamp=timestamp
            )
        elif "/render" in request.endpoint:
            return GatewayResponse(
                status="success", 
                data={"render_id": f"ren_{timestamp}", "message": "Rendering started"},
                timestamp=timestamp
            )
        else:
            return GatewayResponse(
                status="info",
                data={"message": "Capsule service available"},
                timestamp=timestamp
            )
    except Exception as e:
        return GatewayResponse(
            status="error",
            error=str(e),
            timestamp=timestamp
        )

async def route_to_ceremony_service(request: GatewayRequest, timestamp: str):
    """Route requests to ceremony services"""
    try:
        # Simulate ceremony service routing
        if "/dispatch" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"dispatch_id": f"AXF-{timestamp}", "message": "Ceremony dispatched"},
                timestamp=timestamp
            )
        elif "/blessing" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"blessing_id": f"bls_{timestamp}", "message": "Flame blessing granted"},
                timestamp=timestamp
            )
        else:
            return GatewayResponse(
                status="info",
                data={"message": "Ceremony service available"},
                timestamp=timestamp
            )
    except Exception as e:
        return GatewayResponse(
            status="error",
            error=str(e),
            timestamp=timestamp
        )

async def route_to_dominion_service(request: GatewayRequest, timestamp: str):
    """Route requests to dominion services"""
    try:
        # Simulate dominion service routing
        if "/council" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"council_session": f"dom_{timestamp}", "message": "Council session initiated"},
                timestamp=timestamp
            )
        elif "/governance" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"governance_id": f"gov_{timestamp}", "message": "Governance protocol activated"},
                timestamp=timestamp
            )
        else:
            return GatewayResponse(
                status="info",
                data={"message": "Dominion service available"},
                timestamp=timestamp
            )
    except Exception as e:
        return GatewayResponse(
            status="error",
            error=str(e),
            timestamp=timestamp
        )

async def route_to_axiom_service(request: GatewayRequest, timestamp: str):
    """Route requests to axiom flame services"""
    try:
        # Simulate axiom service routing
        if "/reason" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"reasoning_id": f"axm_{timestamp}", "message": "Axiom reasoning initiated"},
                timestamp=timestamp
            )
        elif "/flame" in request.endpoint:
            return GatewayResponse(
                status="success",
                data={"flame_id": f"flm_{timestamp}", "message": "Flame ignited"},
                timestamp=timestamp
            )
        else:
            return GatewayResponse(
                status="info",
                data={"message": "Axiom service available"},
                timestamp=timestamp
            )
    except Exception as e:
        return GatewayResponse(
            status="error",
            error=str(e),
            timestamp=timestamp
        )

@router.get("/status")
async def gateway_status():
    """Get gateway status"""
    return {
        "status": "operational",
        "services": ["capsule", "ceremony", "dominion", "axiom"],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/routes")
async def list_routes():
    """List available gateway routes"""
    return {
        "routes": {
            "/capsule": ["create", "render", "publish"],
            "/ceremony": ["dispatch", "blessing", "replay"],
            "/dominion": ["council", "governance", "outreach"],
            "/axiom": ["reason", "flame", "audit"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }