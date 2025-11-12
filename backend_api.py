#!/usr/bin/env python3
"""
CodexDominion.app - Production Backend
FastAPI backend that matches the TypeScript API client interface
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import datetime
import jwt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = "super-secret-key-for-development"  # In production, use a secure key
ALGORITHM = "HS256"

# Security
security = HTTPBearer()

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str
    username: str
    role: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class WorkflowResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: str
    description: Optional[str] = None

class WorkflowCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class AxiomCeremonyRequest(BaseModel):
    actor: str
    realm: str
    capsule: str
    intent: Optional[str] = None

class AxiomCeremonyResponse(BaseModel):
    dispatch_id: str
    status: str
    timestamp: str
    actor: str
    realm: str
    capsule: str

# FastAPI App
app = FastAPI(
    title="CodexDominion.app Backend",
    version="1.0.0",
    description="Production-Ready FastAPI Backend with TypeScript Integration"
)

# Import and register AXIOM gateway
from app.gateway import router as axiom_router
app.include_router(axiom_router)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",  # React dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data
USERS = {
    "admin": {"id": "user-1", "username": "admin", "password": "secret", "role": "admin"},
    "user": {"id": "user-2", "username": "user", "password": "password", "role": "user"},
    "custodian": {"id": "user-3", "username": "custodian", "password": "secret", "role": "custodian"}
}

WORKFLOWS = [
    WorkflowResponse(
        id="wf-1", 
        name="Data Processing Pipeline", 
        status="running",
        created_at=datetime.datetime.now().isoformat(),
        description="Processing incoming data streams"
    ),
    WorkflowResponse(
        id="wf-2", 
        name="Model Training", 
        status="completed",
        created_at=datetime.datetime.now().isoformat(),
        description="Training ML models on processed data"
    ),
    WorkflowResponse(
        id="wf-3", 
        name="System Backup", 
        status="pending",
        created_at=datetime.datetime.now().isoformat(),
        description="Scheduled system backup operation"
    ),
    WorkflowResponse(
        id="wf-4", 
        name="Security Scan", 
        status="failed",
        created_at=datetime.datetime.now().isoformat(),
        description="Automated security vulnerability scan"
    )
]

# Helper Functions
def create_token(user_data: dict) -> str:
    """Create JWT token for user"""
    payload = {
        "sub": user_data["id"],
        "username": user_data["username"],
        "role": user_data["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Health Endpoints
@app.get("/health/live")
async def health_live():
    """Liveness probe - is the service running?"""
    return {
        "status": "healthy",
        "service": "codexdominion-backend", 
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health/ready") 
async def health_ready():
    """Readiness probe - is the service ready to accept requests?"""
    return {
        "status": "ready",
        "service": "codexdominion-backend",
        "dependencies": {
            "database": "connected",
            "axiom_flame": "available"
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

# Authentication Endpoints
@app.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    user_data = USERS.get(request.username)
    
    if not user_data or user_data["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_token(user_data)
    user = User(
        id=user_data["id"],
        username=user_data["username"], 
        role=user_data["role"]
    )
    
    logger.info(f"User {request.username} logged in successfully")
    
    return AuthResponse(
        access_token=token,
        user=user
    )

@app.get("/auth/me", response_model=User)
async def get_current_user(user_data: dict = Depends(verify_token)):
    """Get current user information"""
    return User(
        id=user_data["sub"],
        username=user_data["username"],
        role=user_data["role"]
    )

@app.post("/auth/logout")
async def logout(user_data: dict = Depends(verify_token)):
    """Logout user (token invalidation would happen here in production)"""
    logger.info(f"User {user_data['username']} logged out")
    return {"message": "Successfully logged out"}

# Workflow Endpoints
@app.get("/workflow", response_model=List[WorkflowResponse])
async def list_workflows(user_data: dict = Depends(verify_token)):
    """List all workflows for authenticated user"""
    logger.info(f"User {user_data['username']} requested workflow list")
    return WORKFLOWS

@app.get("/workflow/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str, user_data: dict = Depends(verify_token)):
    """Get specific workflow by ID"""
    workflow = next((wf for wf in WORKFLOWS if wf.id == workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    logger.info(f"User {user_data['username']} requested workflow {workflow_id}")
    return workflow

@app.post("/workflow", response_model=WorkflowResponse)
async def create_workflow(request: WorkflowCreateRequest, user_data: dict = Depends(verify_token)):
    """Create new workflow"""
    new_workflow = WorkflowResponse(
        id=f"wf-{len(WORKFLOWS) + 1}",
        name=request.name,
        status="pending",
        created_at=datetime.datetime.now().isoformat(),
        description=request.description
    )
    
    WORKFLOWS.append(new_workflow)
    logger.info(f"User {user_data['username']} created workflow {new_workflow.id}")
    
    return new_workflow

@app.post("/workflow/start", response_model=WorkflowResponse)
async def start_workflow(name: str, capsule: Optional[str] = None, user_data: dict = Depends(verify_token)):
    """Start a new workflow with specified name and capsule"""
    new_workflow = WorkflowResponse(
        id=f"wf-{len(WORKFLOWS) + 1}",
        name=name,
        status="running",
        created_at=datetime.datetime.now().isoformat(),
        description=f"Started workflow with capsule: {capsule or 'default'}"
    )
    
    WORKFLOWS.append(new_workflow)
    logger.info(f"User {user_data['username']} started workflow {new_workflow.id} ({name}) with capsule: {capsule}")
    
    return new_workflow

@app.post("/workflow/{workflow_id}/advance", response_model=WorkflowResponse)
async def advance_workflow(workflow_id: str, phase: str, note: Optional[str] = None, user_data: dict = Depends(verify_token)):
    """Advance workflow to next phase"""
    workflow = next((wf for wf in WORKFLOWS if wf.id == workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Update workflow status based on phase
    phase_status_map = {
        "DISPATCH": "running",
        "PROCESS": "running", 
        "VALIDATE": "running",
        "COMPLETE": "completed",
        "ABORT": "failed"
    }
    
    workflow.status = phase_status_map.get(phase, "running")
    workflow.description = f"Advanced to {phase}" + (f" - {note}" if note else "")
    
    logger.info(f"User {user_data['username']} advanced workflow {workflow_id} to phase {phase}")
    
    return workflow

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "CodexDominion.app Backend",
        "version": "1.0.0", 
        "status": "operational",
        "endpoints": {
            "health": "/health/live",
            "auth": "/auth/login",
            "workflows": "/workflow",
            "docs": "/docs"
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8010, reload=True)