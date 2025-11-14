
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import sys
import os
from app.middleware.governance import GovernanceMiddleware
from app.middleware.audit import AuditMiddleware

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

try:
    from api.webhooks import router as webhooks_router
    from api.upload import router as upload_router
    from app.gateway import router as gateway_router
    from app.auth_routes import router as auth_router
    from app.auth import get_user, require_admin, require_council, User
    from app.health import router as health_router
    from capsule_api import router as capsule_router
    from services.dominion.outreach_engagement import router as outreach_router
    import sys
    sys.path.append('..')
    from ceremonial_interface import router as ceremonial_router
except ImportError as e:
    print(f"Import error (using fallbacks): {e}")
    # Create fallback routers
    from fastapi import APIRouter
    
    webhooks_router = APIRouter()
    upload_router = APIRouter()
    gateway_router = APIRouter()
    auth_router = APIRouter()
    health_router = APIRouter()
    capsule_router = APIRouter()
    outreach_router = APIRouter()
    ceremonial_router = APIRouter()
    
    # Create dummy auth functions
    def get_user():
        return {"sub": "anonymous", "roles": []}
    
    def require_admin():
        user = get_user()
        return User(sub=user["sub"], roles=user["roles"])
    
    def require_council():
        user = get_user()
        return User(sub=user["sub"], roles=user["roles"])
    
    class User:
        def __init__(self, **kwargs):
            self.sub = kwargs.get("sub", "anonymous")
            self.roles = kwargs.get("roles", [])


app = FastAPI(
    title="Super-Codex-AI Backend", 
    version="1.0.0",
    description="Backend API for Super-Codex-AI with AXIOM FLAME Integration"
)

# CORS middleware for web client access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001", 
        "http://localhost:8000", "http://127.0.0.1:8000",
        "http://localhost:8010", "http://127.0.0.1:8010"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Governance middleware for authority validation and ceremonial compliance
app.add_middleware(GovernanceMiddleware)

# Audit middleware for request/response logging
app.add_middleware(AuditMiddleware)

# Include routers
app.include_router(health_router, prefix="/health")
app.include_router(auth_router, prefix="/auth")
app.include_router(webhooks_router, prefix="/api/webhooks")
app.include_router(upload_router, prefix="/api")
app.include_router(capsule_router, prefix="/api")
app.include_router(outreach_router)
app.include_router(gateway_router, prefix="/axiom")
app.include_router(ceremonial_router, prefix="/dominion")

# Mount static files for ceremonial interface assets
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static directory may not exist in all environments

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.get("/")
async def root():
    return {
        "message": "Super-Codex-AI Backend - Codex Dominion", 
        "status": "operational",
        "flame_state": "sovereign",
        "ceremonial_interface": "/dominion",
        "motto": "The flame burns sovereign and eternal — forever."
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "super-codex-ai"}

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
