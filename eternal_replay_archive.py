#!/usr/bin/env python3
"""
🔥 Eternal Replay Archive - Codex Dominion Interface 🔥

A comprehensive web interface for managing and replaying ceremonial content
with Sacred Avatar narration and dispatch capabilities.

Features:
- Role-based content filtering
- Time-based search and filtering
- Multiple content types (Scrolls, Capsules, Hymns, Invocations)
- Interactive replay viewer with avatar narration
- Re-dispatch capabilities for ceremonial content
"""

from fastapi import FastAPI, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import uuid
from dataclasses import asdict

# Import our Sacred Avatar system
try:
    from avatar_guide_system import SacredAvatarGuide, AvatarCouncil, AvatarRole, ScriptType
    AVATAR_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️  Avatar system not available - running in archive-only mode")
    AVATAR_SYSTEM_AVAILABLE = False

app = FastAPI(title="🔥 Eternal Replay Archive", version="1.0.0")

# Storage configuration
ARCHIVE_ROOT = Path("eternal_archive")
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

# Create directory structure
for directory in [ARCHIVE_ROOT, STATIC_DIR, TEMPLATES_DIR]:
    directory.mkdir(exist_ok=True)

# Content type directories
CONTENT_DIRS = {
    "scrolls": ARCHIVE_ROOT / "scrolls",
    "capsules": ARCHIVE_ROOT / "capsules", 
    "hymns": ARCHIVE_ROOT / "hymns",
    "invocations": ARCHIVE_ROOT / "invocations",
    "replays": ARCHIVE_ROOT / "replays",
    "dispatches": ARCHIVE_ROOT / "dispatches"
}

for content_dir in CONTENT_DIRS.values():
    content_dir.mkdir(parents=True, exist_ok=True)

# Templates setup
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize Avatar Council if available
if AVATAR_SYSTEM_AVAILABLE:
    try:
        council = AvatarCouncil(storage_root=ARCHIVE_ROOT / "avatar_council")
        
        # Summon archive management avatars
        archive_keeper = council.summon_avatar(
            "Archon Memorialis",
            AvatarRole.CUSTODIAN,
            "I am the keeper of eternal memories, guardian of all that was and shall be again."
        )
        
        narrative_weaver = council.summon_avatar(
            "Saga the Storyteller", 
            AvatarRole.HERALD,
            "Through my words, the past lives again in vivid detail."
        )
        
        dispatch_coordinator = council.summon_avatar(
            "Echo the Dispatcher",
            AvatarRole.COUNCIL_MEMBER,
            "I coordinate the eternal dance of replay and redispatch."
        )
        
        print("🏛️ Avatar Council established for Eternal Replay Archive")
        
    except Exception as e:
        print(f"⚠️  Avatar Council initialization failed: {e}")
        council = None
else:
    council = None

class ContentEntry:
    """Represents a piece of archived content"""
    def __init__(self, content_type: str, title: str, content: str, 
                 role: str = "initiate", metadata: Dict = None):
        self.id = str(uuid.uuid4())
        self.content_type = content_type
        self.title = title
        self.content = content
        self.role = role
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.metadata = metadata or {}
        self.replay_count = 0
        self.last_replayed = None
        self.sacred_binding = self._generate_binding()
    
    def _generate_binding(self) -> str:
        """Generate sacred binding for content integrity"""
        import hashlib
        content_hash = hashlib.sha256(
            f"{self.title}{self.content}{self.timestamp}".encode()
        ).hexdigest()
        return content_hash[:12].upper()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_type": self.content_type,
            "title": self.title,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "replay_count": self.replay_count,
            "last_replayed": self.last_replayed,
            "sacred_binding": self.sacred_binding
        }

class ReplaySession:
    """Represents a replay session with avatar narration"""
    def __init__(self, content_entry: ContentEntry, narrator_role: str = "herald"):
        self.id = str(uuid.uuid4())
        self.content_id = content_entry.id
        self.content_entry = content_entry
        self.narrator_role = narrator_role
        self.start_time = datetime.utcnow().isoformat() + "Z"
        self.narration_log = []
        self.status = "active"
    
    def add_narration(self, speaker: str, message: str):
        """Add narration entry to the replay session"""
        self.narration_log.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "speaker": speaker,
            "message": message
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content_id": self.content_id,
            "content_title": self.content_entry.title,
            "narrator_role": self.narrator_role,
            "start_time": self.start_time,
            "narration_log": self.narration_log,
            "status": self.status
        }

# Archive management functions
def save_content(entry: ContentEntry):
    """Save content entry to archive"""
    content_file = CONTENT_DIRS[entry.content_type] / f"{entry.id}.json"
    with open(content_file, 'w', encoding='utf-8') as f:
        json.dump(entry.to_dict(), f, indent=2)

def load_content(content_type: str, content_id: str) -> Optional[ContentEntry]:
    """Load content entry from archive"""
    content_file = CONTENT_DIRS[content_type] / f"{content_id}.json"
    if not content_file.exists():
        return None
    
    with open(content_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entry = ContentEntry(
        content_type=data["content_type"],
        title=data["title"], 
        content=data["content"],
        role=data["role"],
        metadata=data["metadata"]
    )
    
    # Restore saved fields
    entry.id = data["id"]
    entry.timestamp = data["timestamp"]
    entry.replay_count = data.get("replay_count", 0)
    entry.last_replayed = data.get("last_replayed")
    entry.sacred_binding = data["sacred_binding"]
    
    return entry

def search_content(content_types: List[str] = None, role_filter: str = None,
                  time_filter: str = None, query: str = None) -> List[ContentEntry]:
    """Search archived content with filters"""
    results = []
    
    search_types = content_types or list(CONTENT_DIRS.keys())
    
    for content_type in search_types:
        if content_type in ["replays", "dispatches"]:
            continue
            
        content_dir = CONTENT_DIRS[content_type]
        for content_file in content_dir.glob("*.json"):
            try:
                entry = load_content(content_type, content_file.stem)
                if entry is None:
                    continue
                
                # Apply filters
                if role_filter and entry.role != role_filter:
                    continue
                
                if time_filter:
                    entry_time = datetime.fromisoformat(entry.timestamp.rstrip('Z'))
                    filter_time = datetime.utcnow()
                    
                    if time_filter == "day":
                        filter_time -= timedelta(days=1)
                    elif time_filter == "week":
                        filter_time -= timedelta(weeks=1) 
                    elif time_filter == "month":
                        filter_time -= timedelta(days=30)
                    
                    if entry_time < filter_time:
                        continue
                
                if query:
                    search_text = f"{entry.title} {entry.content}".lower()
                    if query.lower() not in search_text:
                        continue
                
                results.append(entry)
                
            except Exception as e:
                print(f"Error loading {content_file}: {e}")
    
    # Sort by timestamp, newest first
    results.sort(key=lambda x: x.timestamp, reverse=True)
    return results

def save_replay_session(session: ReplaySession):
    """Save replay session to archive"""
    replay_file = CONTENT_DIRS["replays"] / f"{session.id}.json"
    with open(replay_file, 'w', encoding='utf-8') as f:
        json.dump(session.to_dict(), f, indent=2)

# Web interface routes
@app.get("/", response_class=HTMLResponse)
async def main_interface(request: Request):
    """Main Eternal Replay Archive interface"""
    return templates.TemplateResponse("archive_main.html", {
        "request": request,
        "title": "🔥 Eternal Replay Archive",
        "avatar_system_available": AVATAR_SYSTEM_AVAILABLE
    })

@app.get("/api/content/search")
async def api_search_content(
    content_types: str = None,
    role_filter: str = None, 
    time_filter: str = None,
    query: str = None
):
    """API endpoint for searching content"""
    try:
        # Parse content types
        types_list = content_types.split(",") if content_types else None
        
        results = search_content(
            content_types=types_list,
            role_filter=role_filter,
            time_filter=time_filter,
            query=query
        )
        
        return {
            "success": True,
            "results": [entry.to_dict() for entry in results],
            "count": len(results)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/content/upload")
async def api_upload_content(
    content_type: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    role: str = Form("initiate"),
    file: UploadFile = File(None)
):
    """API endpoint for uploading new content"""
    try:
        # Handle file upload if provided
        if file and file.filename:
            file_content = await file.read()
            content = file_content.decode('utf-8')
        
        # Create content entry
        entry = ContentEntry(
            content_type=content_type,
            title=title,
            content=content,
            role=role,
            metadata={"uploaded_via": "web_interface"}
        )
        
        # Save to archive
        save_content(entry)
        
        return {
            "success": True,
            "message": f"Content '{title}' archived successfully",
            "entry_id": entry.id,
            "sacred_binding": entry.sacred_binding
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/content/{content_type}/{content_id}")
async def api_get_content(content_type: str, content_id: str):
    """API endpoint for retrieving specific content"""
    try:
        entry = load_content(content_type, content_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return {
            "success": True,
            "content": entry.to_dict()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/replay/start")
async def api_start_replay(
    content_type: str = Form(...),
    content_id: str = Form(...),
    narrator_role: str = Form("herald")
):
    """API endpoint for starting a replay session with avatar narration"""
    try:
        # Load content
        entry = load_content(content_type, content_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Create replay session
        session = ReplaySession(entry, narrator_role)
        
        # Generate avatar narration if available
        if council:
            try:
                # Select appropriate narrator
                narrator_name = {
                    "custodian": "Archon Memorialis",
                    "herald": "Saga the Storyteller", 
                    "council_member": "Echo the Dispatcher"
                }.get(narrator_role, "Saga the Storyteller")
                
                if narrator_name in council.avatars:
                    narrator = council.avatars[narrator_name]
                    
                    # Generate opening narration
                    opening_script = f"Behold, the eternal archives reveal to us: '{entry.title}'. Let us witness again what was preserved in sacred memory."
                    narrator.add_script(opening_script, ScriptType.CEREMONY)
                    
                    opening_narration = narrator.speak(ScriptType.CEREMONY)
                    session.add_narration(narrator_name, opening_narration)
                    
                    # Generate content introduction
                    intro_script = f"This {entry.content_type} was bound to the eternal flame on {entry.timestamp}. Sacred binding: {entry.sacred_binding}."
                    narrator.add_script(intro_script, ScriptType.TEACHING)
                    
                    intro_narration = narrator.speak(ScriptType.TEACHING)
                    session.add_narration(narrator_name, intro_narration)
                    
            except Exception as e:
                session.add_narration("System", f"Avatar narration error: {e}")
        
        # Update content replay stats
        entry.replay_count += 1
        entry.last_replayed = datetime.utcnow().isoformat() + "Z"
        save_content(entry)
        
        # Save replay session
        save_replay_session(session)
        
        return {
            "success": True,
            "session_id": session.id,
            "narration": session.narration_log,
            "content": entry.to_dict()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/replay/{session_id}/narrate")
async def api_add_narration(
    session_id: str,
    message: str = Form(...),
    script_type: str = Form("guidance")
):
    """API endpoint for adding avatar narration to replay session"""
    try:
        if not council:
            return {"success": False, "error": "Avatar system not available"}
        
        # Load replay session
        replay_file = CONTENT_DIRS["replays"] / f"{session_id}.json"
        if not replay_file.exists():
            raise HTTPException(status_code=404, detail="Replay session not found")
        
        # Get active narrator
        narrator = council.avatars.get("Saga the Storyteller")
        if not narrator:
            return {"success": False, "error": "Narrator avatar not available"}
        
        # Add custom script and speak
        script_type_enum = getattr(ScriptType, script_type.upper(), ScriptType.GUIDANCE)
        narrator.add_script(message, script_type_enum)
        narration = narrator.speak(script_type_enum)
        
        # Update session (simplified - in production would reload full session)
        session_data = {
            "speaker": "Saga the Storyteller",
            "message": narration,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return {
            "success": True,
            "narration": session_data
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/dispatch/again")
async def api_dispatch_again(
    content_type: str = Form(...),
    content_id: str = Form(...),
    dispatch_role: str = Form("herald")
):
    """API endpoint for re-dispatching content"""
    try:
        # Load original content
        entry = load_content(content_type, content_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Create dispatch record
        dispatch_record = {
            "id": str(uuid.uuid4()),
            "original_content_id": content_id,
            "content_type": content_type,
            "dispatch_role": dispatch_role,
            "dispatch_time": datetime.utcnow().isoformat() + "Z",
            "dispatch_authority": dispatch_role,
            "content_snapshot": entry.to_dict()
        }
        
        # Generate dispatch narration if avatars available
        dispatch_messages = []
        if council:
            try:
                dispatcher = council.avatars.get("Echo the Dispatcher")
                if dispatcher:
                    dispatch_script = f"By sacred authority, I dispatch again the {content_type} '{entry.title}' to flow through the eternal currents of the Dominion."
                    dispatcher.add_script(dispatch_script, ScriptType.CEREMONY)
                    
                    dispatch_narration = dispatcher.speak(ScriptType.CEREMONY)
                    dispatch_messages.append({
                        "speaker": "Echo the Dispatcher",
                        "message": dispatch_narration
                    })
                    
            except Exception as e:
                dispatch_messages.append({
                    "speaker": "System",
                    "message": f"Dispatch narration error: {e}"
                })
        
        # Save dispatch record
        dispatch_file = CONTENT_DIRS["dispatches"] / f"{dispatch_record['id']}.json"
        dispatch_record["narration"] = dispatch_messages
        
        with open(dispatch_file, 'w', encoding='utf-8') as f:
            json.dump(dispatch_record, f, indent=2)
        
        return {
            "success": True,
            "dispatch_id": dispatch_record["id"],
            "message": f"Content '{entry.title}' dispatched again successfully",
            "narration": dispatch_messages
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/stats")
async def api_get_stats():
    """API endpoint for archive statistics"""
    try:
        stats = {
            "total_content": 0,
            "by_type": {},
            "by_role": {},
            "total_replays": 0,
            "total_dispatches": 0,
            "avatar_council_active": council is not None
        }
        
        # Count content by type
        for content_type, content_dir in CONTENT_DIRS.items():
            if content_type in ["replays", "dispatches"]:
                if content_type == "replays":
                    stats["total_replays"] = len(list(content_dir.glob("*.json")))
                elif content_type == "dispatches":
                    stats["total_dispatches"] = len(list(content_dir.glob("*.json")))
                continue
            
            count = len(list(content_dir.glob("*.json")))
            stats["by_type"][content_type] = count
            stats["total_content"] += count
        
        # Count by role (simplified)
        for content_type in ["scrolls", "capsules", "hymns", "invocations"]:
            content_dir = CONTENT_DIRS[content_type]
            for content_file in content_dir.glob("*.json"):
                try:
                    with open(content_file, 'r') as f:
                        data = json.load(f)
                        role = data.get("role", "unknown")
                        stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
                except:
                    continue
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

if __name__ == "__main__":
    print("🔥 Starting Eternal Replay Archive...")
    print("="*60)
    
    if AVATAR_SYSTEM_AVAILABLE and council:
        print("🏛️ Avatar Council Active:")
        status = council.get_council_status()
        print(f"   Total Avatars: {status['total_avatars']}")
        for avatar_name in status.get('active_avatars', []):
            print(f"   ✅ {avatar_name}")
    
    print(f"📁 Archive Root: {ARCHIVE_ROOT}")
    print("🌐 Server starting on http://localhost:8002")
    print("="*60)
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)