from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models import RecallEntry, RecallCreate, RecallQuery
import uuid

router = APIRouter()

# In-memory storage for demo purposes
recall_db = {}

@router.get("/", response_model=List[RecallEntry])
async def list_recalls(
    actor: Optional[str] = Query(None),
    realm: Optional[str] = Query(None),
    capsule: Optional[str] = Query(None),
    intent: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    archived: Optional[bool] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0)
):
    """List recall entries with optional filtering"""
    entries = list(recall_db.values())
    
    # Apply filters
    if actor:
        entries = [e for e in entries if e.actor == actor]
    if realm:
        entries = [e for e in entries if e.realm == realm]
    if capsule:
        entries = [e for e in entries if e.capsule == capsule]
    if intent:
        entries = [e for e in entries if intent.lower() in e.intent.lower()]
    if tag:
        entries = [e for e in entries if tag in e.tags]
    if archived is not None:
        entries = [e for e in entries if e.archived == archived]
    
    # Sort by timestamp (newest first)
    entries.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Apply pagination
    return entries[offset:offset + limit]

@router.get("/{recall_id}", response_model=RecallEntry)
async def get_recall(recall_id: str):
    """Get a specific recall entry by ID"""
    if recall_id not in recall_db:
        raise HTTPException(status_code=404, detail="Recall entry not found")
    return recall_db[recall_id]

@router.post("/", response_model=RecallEntry)
async def create_recall(recall: RecallCreate):
    """Create a new recall entry"""
    recall_id = f"rec_{len(recall_db) + 1}"
    
    new_recall = RecallEntry(
        id=recall_id,
        dispatch_id=recall.dispatch_id,
        timestamp=datetime.now(),
        actor=recall.actor,
        realm=recall.realm,
        capsule=recall.capsule,
        intent=recall.intent,
        content=recall.content,
        tags=recall.tags,
        metadata=recall.metadata
    )
    recall_db[recall_id] = new_recall
    return new_recall

@router.post("/search", response_model=List[RecallEntry])
async def search_recalls(query: RecallQuery, limit: int = 100):
    """Advanced search for recall entries"""
    entries = list(recall_db.values())
    
    # Apply filters from query
    if query.actor:
        entries = [e for e in entries if e.actor == query.actor]
    if query.realm:
        entries = [e for e in entries if e.realm == query.realm]
    if query.capsule:
        entries = [e for e in entries if e.capsule == query.capsule]
    if query.intent:
        entries = [e for e in entries if query.intent.lower() in e.intent.lower()]
    if query.tags:
        entries = [e for e in entries if any(tag in e.tags for tag in query.tags)]
    if query.start_date:
        entries = [e for e in entries if e.timestamp >= query.start_date]
    if query.end_date:
        entries = [e for e in entries if e.timestamp <= query.end_date]
    if query.archived is not None:
        entries = [e for e in entries if e.archived == query.archived]
    
    # Sort by timestamp (newest first)
    entries.sort(key=lambda x: x.timestamp, reverse=True)
    
    return entries[:limit]

@router.get("/dispatch/{dispatch_id}", response_model=List[RecallEntry])
async def get_recalls_by_dispatch(dispatch_id: str):
    """Get all recall entries for a specific dispatch ID"""
    entries = [e for e in recall_db.values() if e.dispatch_id == dispatch_id]
    entries.sort(key=lambda x: x.timestamp, reverse=True)
    return entries

@router.put("/{recall_id}/archive")
async def archive_recall(recall_id: str):
    """Archive a recall entry"""
    if recall_id not in recall_db:
        raise HTTPException(status_code=404, detail="Recall entry not found")
    
    recall_db[recall_id].archived = True
    return {"message": "Recall entry archived successfully"}

@router.put("/{recall_id}/restore")
async def restore_recall(recall_id: str):
    """Restore an archived recall entry"""
    if recall_id not in recall_db:
        raise HTTPException(status_code=404, detail="Recall entry not found")
    
    recall_db[recall_id].archived = False
    return {"message": "Recall entry restored successfully"}

@router.delete("/{recall_id}")
async def delete_recall(recall_id: str):
    """Permanently delete a recall entry"""
    if recall_id not in recall_db:
        raise HTTPException(status_code=404, detail="Recall entry not found")
    
    del recall_db[recall_id]
    return {"message": "Recall entry deleted successfully"}

@router.get("/stats/summary")
async def get_recall_stats():
    """Get recall database statistics"""
    total_entries = len(recall_db)
    archived_entries = len([e for e in recall_db.values() if e.archived])
    active_entries = total_entries - archived_entries
    
    # Get unique actors, realms, capsules
    actors = set(e.actor for e in recall_db.values())
    realms = set(e.realm for e in recall_db.values())
    capsules = set(e.capsule for e in recall_db.values())
    
    # Recent activity (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    recent_entries = len([e for e in recall_db.values() if e.timestamp >= yesterday])
    
    return {
        "total_entries": total_entries,
        "active_entries": active_entries,
        "archived_entries": archived_entries,
        "unique_actors": len(actors),
        "unique_realms": len(realms),
        "unique_capsules": len(capsules),
        "recent_entries_24h": recent_entries,
        "timestamp": datetime.now().isoformat()
    }
