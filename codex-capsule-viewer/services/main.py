from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from datetime import datetime
import uuid
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.capsule import Capsule, CapsuleCreate, CapsuleResponse

app = FastAPI(title="Codex Capsule Viewer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demonstration
capsules_db: List[Capsule] = [
    Capsule(
        id="cap_001",
        title="Sovereign Foundation Charter",
        sigil="⚡",
        createdAt=datetime.now(),
        content="The foundational principles of sovereign governance...",
        heirRights=["custodian", "flamekeeper"],
        covenantSeals=["genesis", "authority"]
    ),
    Capsule(
        id="cap_002",
        title="Ceremonial Protocols",
        sigil="🔥",
        createdAt=datetime.now(),
        content="Sacred ceremonies and their proper execution...",
        heirRights=["flamekeeper"],
        covenantSeals=["ritual", "honor"]
    ),
    Capsule(
        id="cap_003",
        title="Honor Ledger Genesis",
        sigil="⚖️",
        createdAt=datetime.now(),
        content="The first entries in the sovereign honor system...",
        heirRights=["custodian", "council"],
        covenantSeals=["honor", "authority", "legacy"]
    )
]

@app.get("/")
async def root():
    return {"message": "Codex Capsule Viewer API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "operational", "timestamp": datetime.now()}

@app.get("/api/capsules", response_model=List[CapsuleResponse])
async def list_capsules():
    """List all available capsules"""
    return [
        CapsuleResponse(
            id=capsule.id,
            title=capsule.title,
            sigil=capsule.sigil,
            createdAt=capsule.createdAt,
            summary=capsule.content[:100] + "..." if capsule.content and len(capsule.content) > 100 else capsule.content
        )
        for capsule in capsules_db
    ]

@app.get("/api/capsules/{capsule_id}", response_model=Capsule)
async def get_capsule(capsule_id: str):
    """Get detailed information about a specific capsule"""
    capsule = next((c for c in capsules_db if c.id == capsule_id), None)
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    return capsule

@app.post("/api/capsules", response_model=Capsule)
async def create_capsule(capsule_data: CapsuleCreate):
    """Create a new capsule"""
    new_capsule = Capsule(
        id=f"cap_{uuid.uuid4().hex[:8]}",
        title=capsule_data.title,
        sigil=capsule_data.sigil,
        createdAt=datetime.now(),
        content=capsule_data.content,
        heirRights=capsule_data.heirRights or [],
        covenantSeals=["genesis"]
    )
    capsules_db.append(new_capsule)
    return new_capsule

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8082)