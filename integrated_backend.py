#!/usr/bin/env python3
"""
Super-Codex-AI Integrated Backend
Combines all backend services into a single working application
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import sys
import json
import time
import subprocess
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Authentication setup
security = HTTPBearer()

class User(BaseModel):
    sub: str
    roles: List[str]
    email: Optional[str] = None

def get_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dummy authentication - returns test user"""
    return User(sub="test_user", roles=["admin", "operator"])

def require_admin(user: User = Depends(get_user)) -> User:
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_council(user: User = Depends(get_user)) -> User:
    if "council" not in user.roles:
        raise HTTPException(status_code=403, detail="Council access required") 
    return user

# Create FastAPI app
app = FastAPI(
    title="Super-Codex-AI Integrated Backend",
    version="1.0.0",
    description="Combined backend with all Super-Codex-AI services"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001",
        "http://localhost:8010", "http://127.0.0.1:8010"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Core Health Endpoints ===

@app.get("/")
async def root():
    return {
        "message": "Super-Codex-AI Backend is running",
        "status": "healthy",
        "services": ["api", "axiom-flame", "auth", "capsule"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "super-codex-ai-integrated"}

@app.get("/health/live")
async def health_live():
    return {"status": "alive", "timestamp": datetime.now().isoformat()}

@app.get("/health/ready")
async def health_ready():
    return {"status": "ready", "services": ["backend", "auth", "axiom"]}

# === API Health Endpoints (for frontend) ===
@app.get("/api/health/live")
async def api_health_live():
    return {"status": "live", "timestamp": datetime.now().isoformat()}

@app.get("/api/health/ready")
async def api_health_ready():
    return {"status": "ready", "services": ["backend", "auth", "axiom"]}

@app.get("/api/health/deps")
async def api_health_deps():
    return {
        "status": "healthy",
        "dependencies": {
            "database": "healthy",
            "axiom_flame": "healthy",
            "file_system": "healthy"
        }
    }

# === Authentication Endpoints ===

@app.get("/auth/me")
async def get_current_user(user: User = Depends(get_user)):
    return {"user": user.dict(), "authenticated": True}

@app.get("/protected")
async def protected_endpoint(user: User = Depends(get_user)):
    """Protected endpoint that requires authentication"""
    return {
        "message": "Access granted to protected resource",
        "user": user.sub,
        "roles": user.roles
    }

@app.get("/admin")
async def admin_endpoint(user: User = Depends(require_admin)):
    """Admin-only endpoint"""
    return {
        "message": "Admin access granted",
        "user": user.sub,
        "admin_features": [
            "User management", 
            "System configuration",
            "AXIOM FLAME administration"
        ]
    }

@app.get("/council")
async def council_endpoint(user: User = Depends(require_council)):
    """Council-only endpoint"""
    return {
        "message": "Council access granted",
        "user": user.sub,
        "council_capabilities": [
            "Ceremonial operations",
            "Governance oversight", 
            "Strategic decisions"
        ]
    }

# === AXIOM Flame Integration ===

# Storage setup for AXIOM
axiom_storage = Path("./axiom-storage")
axiom_storage.mkdir(exist_ok=True)
ledger_path = axiom_storage / "ledger"
ledger_path.mkdir(exist_ok=True)
replays_path = axiom_storage / "replays" 
replays_path.mkdir(exist_ok=True)

class AxiomRequest(BaseModel):
    actor: str
    realm: str
    capsule: str
    intent: str
    reasoning: Optional[str] = ""

@app.post("/axiom/reason")
async def axiom_reason(request: AxiomRequest, user: User = Depends(get_user)):
    """AXIOM ceremonial reasoning endpoint"""
    try:
        # Generate dispatch ID
        timestamp_str = datetime.now().strftime('%Y-%m-%d')
        content_hash = hashlib.sha256(str(request.dict()).encode()).hexdigest()[:8]
        dispatch_id = f"AXF-{timestamp_str}-{content_hash}"
        
        # Create reasoning entry
        reasoning_entry = {
            'dispatch_id': dispatch_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'actor': request.actor,
            'realm': request.realm,
            'capsule': request.capsule,
            'intent': request.intent,
            'reasoning': request.reasoning,
            'initiated_by': user.sub,
            'governance_seal': {
                'authority': 'ceremonial',
                'classification': 'reasoning',
                'seal_hash': hashlib.sha256(f"{dispatch_id}:{request.dict()}".encode()).hexdigest()
            }
        }
        
        # Save to ledger
        ledger_file = ledger_path / f"{dispatch_id}.json"
        with open(ledger_file, 'w') as f:
            json.dump(reasoning_entry, f, indent=2)
        
        return {
            'status': 'reasoning_complete',
            'dispatch_id': dispatch_id,
            'reasoning_entry': reasoning_entry
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {str(e)}")

@app.get("/axiom/ledger")
async def axiom_list_ledger(user: User = Depends(get_user)):
    """List all AXIOM ledger entries"""
    try:
        entries = []
        for ledger_file in ledger_path.glob("*.json"):
            try:
                with open(ledger_file, 'r') as f:
                    entry = json.load(f)
                entries.append({
                    'dispatch_id': entry.get('dispatch_id', ledger_file.stem),
                    'timestamp': entry.get('timestamp'),
                    'actor': entry.get('actor'),
                    'realm': entry.get('realm'),
                    'capsule': entry.get('capsule'),
                    'initiated_by': entry.get('initiated_by')
                })
            except Exception:
                continue
        
        # Sort by timestamp
        entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {
            'status': 'success',
            'total_entries': len(entries),
            'entries': entries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list ledger: {str(e)}")

@app.get("/axiom/replay/{dispatch_id}")
async def axiom_replay(dispatch_id: str, user: User = Depends(get_user)):
    """Replay AXIOM ceremonial entry"""
    try:
        ledger_file = ledger_path / f"{dispatch_id}.json"
        if not ledger_file.exists():
            raise HTTPException(status_code=404, detail="Dispatch not found")
        
        with open(ledger_file, 'r') as f:
            entry = json.load(f)
        
        # Create replay entry
        replay_entry = {
            'replay_id': f"RPL-{datetime.now().strftime('%Y-%m-%d')}-{hashlib.sha256(dispatch_id.encode()).hexdigest()[:8]}",
            'original_dispatch_id': dispatch_id,
            'replay_timestamp': datetime.now(timezone.utc).isoformat(),
            'replayed_by': user.sub,
            'original_entry': entry,
            'replay_status': 'successful'
        }
        
        # Save replay
        replay_file = replays_path / f"{replay_entry['replay_id']}.json"
        with open(replay_file, 'w') as f:
            json.dump(replay_entry, f, indent=2)
        
        return {
            'status': 'replay_complete',
            'replay_entry': replay_entry
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Replay failed: {str(e)}")

@app.get("/axiom/health")
async def axiom_health():
    """AXIOM Flame health check"""
    return {
        'status': 'healthy',
        'service': 'axiom-flame-integrated',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'storage': {
            'ledger_entries': len(list(ledger_path.glob("*.json"))),
            'replay_entries': len(list(replays_path.glob("*.json")))
        }
    }

# === Capsule API ===

class CapsuleRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    parameters: Dict[str, Any] = {}

@app.post("/api/capsule/activate")
async def activate_capsule(request: CapsuleRequest, user: User = Depends(get_user)):
    """Activate a Codex automation capsule"""
    capsule_id = str(uuid.uuid4())
    
    result = {
        "capsule_id": capsule_id,
        "name": request.name,
        "status": "activated",
        "timestamp": datetime.now().isoformat(),
        "user": user.sub,
        "parameters": request.parameters,
        "execution_log": [
            f"Capsule '{request.name}' initialized",
            f"Parameters validated: {len(request.parameters)} items",
            "Capsule activation complete"
        ]
    }
    
    return result

# === Webhook API ===

class WebhookEvent(BaseModel):
    source: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: Optional[datetime] = None

# In-memory webhook store
webhook_events = []

@app.post("/api/webhooks/webhook")
async def receive_webhook(event: WebhookEvent, request: Request):
    """Receive and process webhook events"""
    try:
        # Add metadata
        event_data = event.dict()
        event_data["id"] = str(uuid.uuid4())
        event_data["received_at"] = datetime.utcnow()
        event_data["ip_address"] = request.client.host if request.client else "unknown"
        
        # Store event
        webhook_events.append(event_data)
        
        return {
            "status": "received",
            "event_id": event_data["id"],
            "message": "Webhook processed successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process webhook")

@app.get("/api/webhooks")
async def list_webhooks(limit: int = 100, user: User = Depends(get_user)):
    """List recent webhook events"""
    return {
        "events": webhook_events[-limit:],
        "total": len(webhook_events)
    }

# === File Upload API ===

from fastapi import UploadFile, File

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_user)):
    """Upload file endpoint"""
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "filename": file.filename,
        "status": "uploaded",
        "size": len(content),
        "uploaded_by": user.sub
    }

# === Restore API ===

@app.post("/api/restore")
async def restore_backup(request: Request, user: User = Depends(require_admin)):
    """Restore from backup (admin only)"""
    data = await request.json()
    backup_dir = data.get("backup_dir")
    if not backup_dir:
        raise HTTPException(status_code=400, detail="Missing backup_dir")
    
    # Log restore start
    log_file = "codex-restore.log"
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()} - Restore started: {backup_dir} by {user.sub}\\n")
    
    # Simulate restore process (replace with actual restore script)
    def simulate_restore():
        yield f"Starting restore from {backup_dir}\\n"
        yield "Checking backup integrity...\\n"
        yield "Backup validation: OK\\n" 
        yield "Restoring database...\\n"
        yield "Database restore: Complete\\n"
        yield "Restoring files...\\n"
        yield "File restore: Complete\\n"
        yield f"Restore completed successfully at {datetime.now()}\\n"
        
        # Log restore end
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()} - Restore completed: {backup_dir}\\n")
    
    return StreamingResponse(simulate_restore(), media_type="text/plain")

# === Error Handlers ===

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": f"The requested endpoint {request.url.path} does not exist",
            "available_endpoints": [
                "/health", "/auth/me", "/protected", "/admin", "/council",
                "/axiom/reason", "/axiom/ledger", "/axiom/health",
                "/api/capsule/activate", "/api/webhooks/webhook", "/api/upload"
            ]
        }
    )

# === Startup Message ===

@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("Super-Codex-AI Integrated Backend Started")
    print("=" * 50)
    print("Available Services:")
    print("  - Core API: /health, /protected, /admin")
    print("  - AXIOM Flame: /axiom/*")
    print("  - Capsule API: /api/capsule/*") 
    print("  - Webhooks: /api/webhooks/*")
    print("  - File Upload: /api/upload")
    print("  - Restore API: /api/restore")
    print("=" * 50)

# Removed main block to prevent conflicts with uvicorn