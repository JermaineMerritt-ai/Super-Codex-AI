"""
Artifacts router for the AXIOM-FLAME ceremonial system.

This module handles Constitutional documents, ceremonial texts, and governance artifacts
with version control, sealing mechanisms, and secure storage management.
"""

from fastapi import APIRouter, HTTPException
from app.models import ArtifactCreate, Artifact
import hashlib
import uuid
import datetime

router = APIRouter()

# In-memory stub (replace with DB)
ARTIFACTS = {}

@router.post("", response_model=Artifact)
def create_artifact(payload: ArtifactCreate):
    """
    Create a new ceremonial artifact.
    
    Args:
        payload: Artifact creation data including type, title, slug, and content URI
        
    Returns:
        Artifact: The created artifact with generated ID, checksum, and metadata
        
    Example:
        POST /artifacts
        {
            "type": "constitution",
            "title": "Axiom Charter",
            "slug": "axiom-charter",
            "content_uri": "s3://ceremonial/axiom-charter.md"
        }
    """
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


@router.post("/{artifact_id}/seal", response_model=Artifact)
def seal_artifact(artifact_id: str):
    """
    Seal an artifact to make it immutable and ceremonially active.
    
    Args:
        artifact_id: The UUID of the artifact to seal
        
    Returns:
        Artifact: The sealed artifact with updated status
        
    Raises:
        HTTPException: 404 if artifact not found
        
    Note:
        Sealing an artifact changes its status from 'draft' to 'sealed',
        making it immutable and ready for ceremonial use.
    """
    obj = ARTIFACTS.get(artifact_id)
    if not obj:
        raise HTTPException(404, "Artifact not found")
    
    obj.status = "sealed"
    # bump version if needed
    ARTIFACTS[artifact_id] = obj
    return obj


@router.get("")
def list_artifacts(type: str | None = None, status: str | None = None):
    """
    List ceremonial artifacts with optional filtering.
    
    Args:
        type: Filter by artifact type (constitution, ritual, oath, seal)
        status: Filter by status (draft, sealed, archived)
        
    Returns:
        list[Artifact]: List of artifacts matching the filter criteria
        
    Example:
        GET /artifacts?type=constitution&status=sealed
    """
    items = list(ARTIFACTS.values())
    if type: 
        items = [a for a in items if a.type == type]
    if status: 
        items = [a for a in items if a.status == status]
    return items


@router.get("/{artifact_id}", response_model=Artifact)
def get_artifact(artifact_id: str):
    """
    Retrieve a specific artifact by ID.
    
    Args:
        artifact_id: The UUID of the artifact to retrieve
        
    Returns:
        Artifact: The requested artifact
        
    Raises:
        HTTPException: 404 if artifact not found
    """
    obj = ARTIFACTS.get(artifact_id)
    if not obj:
        raise HTTPException(404, "Artifact not found")
    return obj


@router.delete("/{artifact_id}")
def delete_artifact(artifact_id: str):
    """
    Delete an artifact (only allowed for draft status).
    
    Args:
        artifact_id: The UUID of the artifact to delete
        
    Returns:
        dict: Success confirmation message
        
    Raises:
        HTTPException: 404 if artifact not found, 403 if artifact is sealed
    """
    obj = ARTIFACTS.get(artifact_id)
    if not obj:
        raise HTTPException(404, "Artifact not found")
    
    if obj.status == "sealed":
        raise HTTPException(403, "Cannot delete sealed artifacts")
    
    del ARTIFACTS[artifact_id]
    return {"message": "Artifact deleted successfully"}
