#!/usr/bin/env python3
"""
Simple test server to verify the API endpoint works
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import hashlib
import uuid
import datetime

app = FastAPI(title="Test API", version="1.0.0")

# In-memory storage
ARTIFACTS = {}

class ArtifactCreate(BaseModel):
    type: Literal["Constitution","Declaration","Anthem","Oath","Ceremony","Handbook","Guide","Proclamation","Compendium","Charter"]
    title: str
    slug: str
    content_uri: str

class Artifact(BaseModel):
    id: str
    type: str
    title: str
    slug: str
    version: str
    status: Literal["draft","sealed","proclaimed"]
    checksum: str
    storage_uri: str
    created_by: str
    created_at: datetime.datetime

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/artifacts")
def list_artifacts():
    return list(ARTIFACTS.values())

@app.get("/v1/artifacts/{artifact_id}", response_model=Artifact)
def get_artifact(artifact_id: str):
    # First try by ID, then by slug
    obj = ARTIFACTS.get(artifact_id)
    if not obj:
        # Try to find by slug
        for artifact in ARTIFACTS.values():
            if artifact.slug == artifact_id:
                obj = artifact
                break
    
    if not obj:
        from fastapi import HTTPException
        raise HTTPException(404, "Artifact not found")
    return obj

@app.post("/v1/artifacts", response_model=Artifact)
def create_artifact(payload: ArtifactCreate):
    aid = str(uuid.uuid4())
    checksum = hashlib.sha256(payload.content_uri.encode()).hexdigest()
    obj = Artifact(
        id=aid, 
        type=payload.type, 
        title=payload.title, 
        slug=payload.slug,
        version="1.0.0", 
        status="draft", 
        checksum=checksum,
        storage_uri=payload.content_uri, 
        created_by="council", 
        created_at=datetime.datetime.utcnow()
    )
    ARTIFACTS[aid] = obj
    return obj

@app.patch("/v1/artifacts/{artifact_id}", response_model=Artifact)
def update_artifact(artifact_id: str, updates: dict):
    # First try by ID, then by slug
    obj = ARTIFACTS.get(artifact_id)
    artifact_key = artifact_id
    
    if not obj:
        # Try to find by slug
        for key, artifact in ARTIFACTS.items():
            if artifact.slug == artifact_id:
                obj = artifact
                artifact_key = key
                break
    
    if not obj:
        from fastapi import HTTPException
        raise HTTPException(404, "Artifact not found")
    
    # Update seals if provided
    if "seals" in updates:
        seals = updates["seals"]
        if "checksum_sha256" in seals:
            obj.checksum = seals["checksum_sha256"]
    
    ARTIFACTS[artifact_key] = obj
    return obj

@app.post("/v1/artifacts/{artifact_id}/seal", response_model=Artifact)
def seal_artifact(artifact_id: str):
    # First try by ID, then by slug
    obj = ARTIFACTS.get(artifact_id)
    artifact_key = artifact_id
    
    if not obj:
        # Try to find by slug
        for key, artifact in ARTIFACTS.items():
            if artifact.slug == artifact_id:
                obj = artifact
                artifact_key = key
                break
    
    if not obj:
        from fastapi import HTTPException
        raise HTTPException(404, "Artifact not found")
    
    # Seal the artifact by changing status
    obj.status = "sealed"
    ARTIFACTS[artifact_key] = obj
    return obj

@app.post("/v1/artifacts/{artifact_id}/proclaim", response_model=Artifact)
def proclaim_artifact(artifact_id: str):
    # First try by ID, then by slug
    obj = ARTIFACTS.get(artifact_id)
    artifact_key = artifact_id
    
    if not obj:
        # Try to find by slug
        for key, artifact in ARTIFACTS.items():
            if artifact.slug == artifact_id:
                obj = artifact
                artifact_key = key
                break
    
    if not obj:
        from fastapi import HTTPException
        raise HTTPException(404, "Artifact not found")
    
    # Only sealed artifacts can be proclaimed
    if obj.status != "sealed":
        from fastapi import HTTPException
        raise HTTPException(400, "Artifact must be sealed before it can be proclaimed")
    
    # Proclaim the artifact by changing status
    obj.status = "proclaimed"
    ARTIFACTS[artifact_key] = obj
    return obj

if __name__ == "__main__":
    print("Starting test server...")
    uvicorn.run("test_server:app", host="localhost", port=8080, reload=True)