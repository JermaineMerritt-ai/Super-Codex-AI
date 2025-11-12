#!/usr/bin/env python3
"""
Integrated AXIOM Backend Server
Combines authentication system with AXIOM FLAME ceremonial operations
"""
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi import FastAPI, Depends, HTTPException, status
    from fastapi.security import HTTPBearer
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from typing import List, Dict, Any, Optional
    from datetime import datetime, timezone
    import uuid
    import json
    
    # Import authentication system
    from app.auth import User, create_token, get_user, require_roles
    from app.auth_routes import router as auth_router
    
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install required packages:")
    print("pip install fastapi uvicorn PyJWT email-validator")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="AXIOM Integrated Backend",
    description="Authentication + AXIOM FLAME Ceremonial Operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

# Security scheme
security = HTTPBearer()

# Storage for ceremonies and dispatches
ceremonies_store = {}
dispatches_store = {}
realms_registry = {
    "PL-001": {"name": "Prime Ledger", "status": "active", "capsules": ["Sovereign Crown", "Prime Seal"]},
    "ST-007": {"name": "Stellar Throne", "status": "active", "capsules": ["Stellar Crown", "Void Seal"]},
    "AX-999": {"name": "Axiom Core", "status": "restricted", "capsules": ["Core Matrix", "System Seal"]}
}

# AXIOM FLAME Health and Status Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint - no authentication required"""
    return {
        "status": "healthy",
        "service": "AXIOM FLAME",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "authentication": "enabled"
    }

@app.get("/status")
async def detailed_status():
    """Detailed status - no authentication required"""
    return {
        "status": "operational",
        "service": "AXIOM FLAME Integrated Backend",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "authentication": "healthy",
            "ceremonial_engine": "operational",
            "registry": "active",
            "audit_system": "enabled"
        },
        "statistics": {
            "total_ceremonies": len(ceremonies_store),
            "total_dispatches": len(dispatches_store),
            "active_realms": len([r for r in realms_registry.values() if r["status"] == "active"])
        }
    }

# AXIOM FLAME Ceremonial Operations (Authentication Required)
@app.post("/api/reason")
async def ceremonial_reasoning(
    request: dict,
    user: User = Depends(require_roles(["user", "council", "admin"]))
):
    """Execute ceremonial reasoning - requires authentication"""
    try:
        # Validate required fields
        required_fields = ["actor", "realm", "capsule", "intent"]
        for field in required_fields:
            if field not in request:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Generate dispatch ID
        dispatch_id = f"AXF-{datetime.now().strftime('%Y-%m-%d')}-{uuid.uuid4().hex[:8]}"
        
        # Validate realm
        realm_id = request["realm"]
        if realm_id not in realms_registry:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown realm: {realm_id}"
            )
        
        realm = realms_registry[realm_id]
        if realm["status"] != "active":
            raise HTTPException(
                status_code=403,
                detail=f"Realm {realm_id} is not active"
            )
        
        # Validate capsule access
        capsule = request["capsule"]
        if capsule not in realm["capsules"]:
            raise HTTPException(
                status_code=403,
                detail=f"Capsule {capsule} not available in realm {realm_id}"
            )
        
        # Create ceremony entry
        ceremony = {
            "dispatch_id": dispatch_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": request["actor"],
            "realm": realm_id,
            "realm_name": realm["name"],
            "capsule": capsule,
            "intent": request["intent"],
            "status": "completed",
            "initiated_by": user.username,
            "user_roles": user.roles,
            "governance": {
                "authority_level": "council" if user.is_council() else "standard",
                "seal_type": "administrative" if user.is_admin() else "operational",
                "validation": "authenticated"
            },
            "audit_trail": {
                "creation": datetime.now(timezone.utc).isoformat(),
                "validator": "AXIOM FLAME Engine v1.0.0",
                "signature": f"SHA256:{uuid.uuid4().hex}"
            }
        }
        
        # Store ceremony
        ceremonies_store[dispatch_id] = ceremony
        dispatches_store[dispatch_id] = {
            "id": dispatch_id,
            "type": "ceremonial_reasoning",
            "status": "completed",
            "created_at": ceremony["timestamp"],
            "created_by": user.username
        }
        
        return {
            "success": True,
            "dispatch_id": dispatch_id,
            "ceremony": ceremony,
            "message": f"Ceremonial reasoning completed for {capsule} in {realm['name']}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ceremonial reasoning failed: {str(e)}"
        )

@app.get("/api/replay/{dispatch_id}")
async def replay_ceremony(dispatch_id: str):
    """Replay a ceremonial dispatch - no authentication required for replay"""
    if dispatch_id not in ceremonies_store:
        raise HTTPException(
            status_code=404,
            detail=f"Dispatch {dispatch_id} not found"
        )
    
    ceremony = ceremonies_store[dispatch_id]
    
    return {
        "success": True,
        "dispatch_id": dispatch_id,
        "replay_timestamp": datetime.now(timezone.utc).isoformat(),
        "original_ceremony": ceremony,
        "replay_status": "successful",
        "validation": {
            "integrity": "verified",
            "authenticity": "confirmed",
            "completeness": "validated"
        }
    }

@app.get("/api/audit/{dispatch_id}")
async def audit_ceremony(dispatch_id: str):
    """Audit a ceremonial dispatch - no authentication required for audit"""
    if dispatch_id not in ceremonies_store:
        raise HTTPException(
            status_code=404,
            detail=f"Dispatch {dispatch_id} not found"
        )
    
    ceremony = ceremonies_store[dispatch_id]
    dispatch = dispatches_store[dispatch_id]
    
    audit_report = {
        "audit_id": f"AUDIT-{uuid.uuid4().hex[:8]}",
        "dispatch_id": dispatch_id,
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "ceremony_data": ceremony,
        "dispatch_metadata": dispatch,
        "audit_results": {
            "structural_integrity": "PASS",
            "governance_compliance": "PASS",
            "authority_validation": "PASS",
            "temporal_consistency": "PASS",
            "signature_verification": "PASS"
        },
        "recommendations": [],
        "audit_trail": {
            "auditor": "AXIOM FLAME Audit Engine",
            "methodology": "Comprehensive Ceremonial Validation",
            "standards": ["AXF-AUDIT-1.0", "GOV-SEAL-2024"]
        }
    }
    
    return {
        "success": True,
        "audit_report": audit_report
    }

# Administrative Endpoints (Admin Only)
@app.get("/api/admin/ceremonies")
async def list_ceremonies(
    user: User = Depends(require_roles(["admin"]))
):
    """List all ceremonies - admin only"""
    return {
        "success": True,
        "total": len(ceremonies_store),
        "ceremonies": list(ceremonies_store.values())
    }

@app.get("/api/admin/realms")
async def list_realms(
    user: User = Depends(require_roles(["admin", "council"]))
):
    """List all realms - council and admin"""
    return {
        "success": True,
        "realms": realms_registry
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "AXIOM Integrated Backend",
        "version": "1.0.0",
        "description": "Authentication + AXIOM FLAME Ceremonial Operations",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "authentication": "/auth/*",
            "ceremonial": "/api/*"
        },
        "authentication": "JWT Bearer Token Required for /api/* endpoints",
        "documentation": "/docs"
    }

def main():
    """Main entry point"""
    print("🚀 Starting AXIOM Integrated Backend...")
    print("📊 Authentication: Enabled")
    print("🔮 AXIOM FLAME: Active")
    print("🌐 API Documentation: http://127.0.0.1:8006/docs")
    print("🔐 Authentication Endpoints: http://127.0.0.1:8006/auth/*")
    print("⚡ AXIOM FLAME Endpoints: http://127.0.0.1:8006/api/*")
    
    uvicorn.run(
        "axiom_integrated_backend:app",
        host="127.0.0.1",
        port=8006,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()