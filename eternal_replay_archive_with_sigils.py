#!/usr/bin/env python3
"""
🔥 Eternal Replay Archive with SIGIL Seal Authentication 🔥

A comprehensive web interface for managing and replaying ceremonial content
with Sacred Avatar narration, SIGIL seal authentication, and dispatch capabilities.

Features:
- Role-based content filtering with SIGIL seal verification
- Cryptographic content authentication via SIGIL seals
- Time-based search and filtering
- Multiple content types (Scrolls, Capsules, Hymns, Invocations)
- Interactive replay viewer with avatar narration
- Re-dispatch capabilities with new ceremonial bindings
- Authority-based seal creation and verification
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
import hashlib
from dataclasses import asdict

# Import our Sacred Avatar system
try:
    from avatar_guide_system import SacredAvatarGuide, AvatarCouncil, AvatarRole, ScriptType
    AVATAR_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️  Avatar system not available - running in archive-only mode")
    AVATAR_SYSTEM_AVAILABLE = False

# Import SIGIL Seal system
try:
    from sigil_seal_system import SIGILSeal, SealRegistry, SealAuthority, CycleType, create_supreme_seal
    SIGIL_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️  SIGIL Seal system not available - running without cryptographic seals")
    SIGIL_SYSTEM_AVAILABLE = False

app = FastAPI(title="🔥 Eternal Replay Archive", version="2.0.0")

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
    "dispatches": ARCHIVE_ROOT / "dispatches",
    "sigil_seals": ARCHIVE_ROOT / "sigil_seals"
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

# Initialize SIGIL Seal Registry if available
if SIGIL_SYSTEM_AVAILABLE:
    try:
        sigil_registry = SealRegistry(str(CONTENT_DIRS["sigil_seals"]))
        print("🔥 SIGIL Seal System initialized for ceremonial authentication")
    except Exception as e:
        print(f"⚠️  SIGIL Seal System initialization failed: {e}")
        sigil_registry = None
        SIGIL_SYSTEM_AVAILABLE = False
else:
    sigil_registry = None

class ContentEntry:
    """Represents a piece of archived content with SIGIL seal authentication"""
    def __init__(self, content_type: str, title: str, content: str, 
                 role: str = "initiate", metadata: Dict = None, custodian_name: str = "Archive System"):
        self.id = str(uuid.uuid4())
        self.content_type = content_type
        self.title = title
        self.content = content
        self.role = role
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.replay_count = 0
        self.dispatch_count = 0
        self.custodian_name = custodian_name
        
        # Generate sacred binding
        binding_data = f"{self.id}:{title}:{role}:{self.created_at.isoformat()}"
        self.sacred_binding = hashlib.sha256(binding_data.encode()).hexdigest()[:16]
        
        # Create SIGIL seal if system is available
        self.sigil_seal_id = None
        self.seal_signature = None
        if SIGIL_SYSTEM_AVAILABLE and sigil_registry:
            self._create_sigil_seal()
    
    def _create_sigil_seal(self):
        """Create a SIGIL seal for this content entry."""
        try:
            # Map roles to seal authorities
            role_authority_map = {
                "custodian": SealAuthority.SUPREME,
                "council_member": SealAuthority.HIGH,
                "flame_keeper": SealAuthority.SACRED,
                "wisdom_bearer": SealAuthority.NOBLE,
                "guardian": SealAuthority.GUARDIAN,
                "ceremonial_guide": SealAuthority.CEREMONIAL,
                "herald": SealAuthority.HERALD,
                "initiate": SealAuthority.INITIATE
            }
            
            authority = role_authority_map.get(self.role, SealAuthority.INITIATE)
            content_hash = hashlib.sha256(self.content.encode()).hexdigest()[:16]
            
            # Create SIGIL seal
            sigil_seal = SIGILSeal(
                custodian_name=self.custodian_name,
                avatar_role=self.role.replace("_", " ").title(),
                cycle_tag=f"{self.content_type.title()} Preservation",
                cycle_type=CycleType.ETERNAL,
                authority=authority,
                content_hash=content_hash
            )
            
            # Register the seal
            if sigil_registry.register_seal(sigil_seal):
                self.sigil_seal_id = sigil_seal.seal_id
                self.seal_signature = sigil_seal.signature
                self.metadata["sigil_glyph"] = sigil_seal.generate_flame_glyph()
                self.metadata["binding_sigil"] = sigil_seal.generate_binding_sigil()
                self.metadata["seal_authority"] = authority.value
                self.metadata["binding_strength"] = sigil_seal.metadata.binding_strength
                
        except Exception as e:
            print(f"Warning: Could not create SIGIL seal: {e}")
    
    def get_sigil_verification(self) -> Dict[str, Any]:
        """Get SIGIL seal verification information."""
        if not SIGIL_SYSTEM_AVAILABLE or not self.sigil_seal_id:
            return {"available": False}
        
        seal = sigil_registry.get_seal(self.sigil_seal_id)
        if not seal:
            return {"available": True, "error": "Seal not found in registry"}
        
        return {
            "available": True,
            "seal_id": seal.seal_id,
            "flame_glyph": seal.generate_flame_glyph(),
            "binding_sigil": seal.generate_binding_sigil(),
            "valid": seal.verify_seal(),
            "authority": seal.authority.value,
            "binding_strength": seal.metadata.binding_strength,
            "ceremonial_weight": seal.metadata.ceremonial_weight,
            "issued_at": seal.issued_at.isoformat(),
            "custodian": seal.custodian_name,
            "cycle_type": seal.cycle_type.value
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/API responses."""
        result = {
            "id": self.id,
            "content_type": self.content_type,
            "title": self.title,
            "content": self.content,
            "role": self.role,
            "sacred_binding": self.sacred_binding,
            "created_at": self.created_at.isoformat(),
            "replay_count": self.replay_count,
            "dispatch_count": self.dispatch_count,
            "metadata": self.metadata,
            "sigil_seal_id": self.sigil_seal_id,
            "custodian_name": self.custodian_name
        }
        
        # Add SIGIL verification if available
        sigil_verification = self.get_sigil_verification()
        if sigil_verification["available"]:
            result["sigil_verification"] = sigil_verification
        
        return result

class ReplaySession:
    """Manages a replay session with avatar narration"""
    def __init__(self, content_entry: ContentEntry, narrator_role: str = "herald"):
        self.session_id = str(uuid.uuid4())
        self.content_id = content_entry.id
        self.content_entry = content_entry
        self.narrator_role = narrator_role
        self.started_at = datetime.now()
        self.narration_log = []
        self.is_active = True
        
        # Add initial narration
        if AVATAR_SYSTEM_AVAILABLE and council:
            self._add_initial_narration()
        else:
            self.narration_log.append({
                "speaker": "Archive System",
                "message": f"Beginning replay of {content_entry.content_type}: {content_entry.title}",
                "timestamp": datetime.now().isoformat(),
                "script_type": "guidance"
            })
    
    def _add_initial_narration(self):
        """Add initial avatar narration."""
        try:
            # Get appropriate avatar for narration
            if self.narrator_role == "herald" and narrative_weaver:
                narrator = narrative_weaver
            elif self.narrator_role == "custodian" and archive_keeper:
                narrator = archive_keeper
            elif dispatch_coordinator:
                narrator = dispatch_coordinator
            else:
                narrator = None
            
            if narrator:
                initial_script = narrator.generate_script(
                    ScriptType.GUIDANCE,
                    f"We now begin the sacred replay of this {self.content_entry.content_type}"
                )
                
                self.narration_log.append({
                    "speaker": narrator.name,
                    "message": initial_script,
                    "timestamp": datetime.now().isoformat(),
                    "script_type": "guidance"
                })
                
        except Exception as e:
            print(f"Warning: Could not add initial narration: {e}")
    
    def add_narration(self, message: str, script_type: str = "guidance") -> bool:
        """Add custom narration to the session."""
        try:
            if not self.is_active:
                return False
            
            narrator_name = "User"
            if AVATAR_SYSTEM_AVAILABLE and council:
                # Try to get appropriate avatar
                if self.narrator_role == "herald" and narrative_weaver:
                    narrator = narrative_weaver
                    enhanced_script = narrator.generate_script(ScriptType.GUIDANCE, message)
                    narrator_name = narrator.name
                    message = enhanced_script
            
            self.narration_log.append({
                "speaker": narrator_name,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "script_type": script_type
            })
            
            return True
            
        except Exception as e:
            print(f"Error adding narration: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "content_id": self.content_id,
            "content": self.content_entry.to_dict(),
            "narrator_role": self.narrator_role,
            "started_at": self.started_at.isoformat(),
            "is_active": self.is_active,
            "narration": self.narration_log
        }

# Global storage
content_storage: Dict[str, Dict[str, ContentEntry]] = {
    content_type: {} for content_type in CONTENT_DIRS.keys() if content_type not in ["replays", "dispatches", "sigil_seals"]
}
replay_sessions: Dict[str, ReplaySession] = {}

def load_existing_content():
    """Load existing content from storage."""
    for content_type, storage_dict in content_storage.items():
        content_dir = CONTENT_DIRS.get(content_type)
        if content_dir and content_dir.exists():
            for content_file in content_dir.glob("*.json"):
                try:
                    with open(content_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert to ContentEntry object
                    entry = ContentEntry(
                        content_type=data["content_type"],
                        title=data["title"],
                        content=data["content"],
                        role=data.get("role", "initiate"),
                        metadata=data.get("metadata", {}),
                        custodian_name=data.get("custodian_name", "Archive System")
                    )
                    
                    # Restore saved values
                    entry.id = data["id"]
                    entry.sacred_binding = data["sacred_binding"]
                    entry.created_at = datetime.fromisoformat(data["created_at"])
                    entry.replay_count = data.get("replay_count", 0)
                    entry.dispatch_count = data.get("dispatch_count", 0)
                    entry.sigil_seal_id = data.get("sigil_seal_id")
                    
                    storage_dict[entry.id] = entry
                    
                except Exception as e:
                    print(f"Warning: Could not load {content_file}: {e}")

def save_content_entry(entry: ContentEntry):
    """Save a content entry to persistent storage."""
    try:
        content_dir = CONTENT_DIRS[entry.content_type]
        file_path = content_dir / f"{entry.id}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(entry.to_dict(), f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error saving content entry: {e}")

def search_content(content_types: List[str] = None, role_filter: str = None, 
                  time_filter: str = None, query: str = None) -> List[ContentEntry]:
    """Search and filter content based on criteria."""
    results = []
    
    # Default to all content types if none specified
    if not content_types:
        content_types = list(content_storage.keys())
    
    for content_type in content_types:
        if content_type in content_storage:
            for entry in content_storage[content_type].values():
                # Apply filters
                if role_filter and entry.role != role_filter:
                    continue
                
                if time_filter:
                    cutoff = datetime.now()
                    if time_filter == "day":
                        cutoff -= timedelta(days=1)
                    elif time_filter == "week":
                        cutoff -= timedelta(weeks=1)
                    elif time_filter == "month":
                        cutoff -= timedelta(days=30)
                    
                    if entry.created_at < cutoff:
                        continue
                
                if query:
                    search_text = f"{entry.title} {entry.content}".lower()
                    if query.lower() not in search_text:
                        continue
                
                results.append(entry)
    
    # Sort by creation date, newest first
    results.sort(key=lambda x: x.created_at, reverse=True)
    return results

# Load existing content on startup
load_existing_content()
print(f"🔥 Starting Eternal Replay Archive...")
print("=" * 60)
if AVATAR_SYSTEM_AVAILABLE and council:
    print(f"🏛️ Avatar Council Active:")
    print(f"   Total Avatars: {len(council.avatars)}")
    for avatar in council.avatars.values():
        print(f"   ✅ {avatar.name}")
if SIGIL_SYSTEM_AVAILABLE and sigil_registry:
    stats = sigil_registry.get_registry_stats()
    print(f"🔥 SIGIL Seal Registry Active:")
    print(f"   Total Seals: {stats.get('total_seals', 0)}")
    
print(f"📁 Archive Root: {ARCHIVE_ROOT}")
print(f"🌐 Server starting on http://localhost:8002")
print("=" * 60)

@app.get("/", response_class=HTMLResponse)
async def main_interface(request: Request):
    """Main archive interface."""
    return templates.TemplateResponse("archive_main.html", {
        "request": request,
        "title": "🔥 Eternal Replay Archive",
        "avatar_system_available": AVATAR_SYSTEM_AVAILABLE,
        "sigil_system_available": SIGIL_SYSTEM_AVAILABLE
    })

@app.get("/api/content/search")
async def api_search_content(
    content_types: str = None,
    role_filter: str = None,
    time_filter: str = None,
    query: str = None
):
    """Search content with filters."""
    try:
        # Parse content types
        types_list = None
        if content_types:
            types_list = [t.strip() for t in content_types.split(",")]
        
        results = search_content(types_list, role_filter, time_filter, query)
        
        return {
            "success": True,
            "results": [entry.to_dict() for entry in results],
            "total": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content/upload")
async def api_upload_content(
    content_type: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    role: str = Form("initiate"),
    custodian_name: str = Form("Archive System"),
    file: UploadFile = File(None)
):
    """Upload new content to the archive."""
    try:
        # If file is provided, read its content
        if file:
            file_content = await file.read()
            content = file_content.decode('utf-8')
        
        if not content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        # Create content entry
        entry = ContentEntry(
            content_type=content_type,
            title=title,
            content=content,
            role=role,
            custodian_name=custodian_name
        )
        
        # Store in memory and persistent storage
        if content_type in content_storage:
            content_storage[content_type][entry.id] = entry
            save_content_entry(entry)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid content type: {content_type}")
        
        return {
            "success": True,
            "content_id": entry.id,
            "sacred_binding": entry.sacred_binding,
            "sigil_verification": entry.get_sigil_verification() if SIGIL_SYSTEM_AVAILABLE else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/content/{content_type}/{content_id}")
async def api_get_content(content_type: str, content_id: str):
    """Get specific content by type and ID."""
    try:
        if content_type not in content_storage:
            raise HTTPException(status_code=404, detail="Content type not found")
        
        entry = content_storage[content_type].get(content_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return {"success": True, "content": entry.to_dict()}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/replay/start")
async def api_start_replay(
    content_type: str = Form(...),
    content_id: str = Form(...),
    narrator_role: str = Form("herald")
):
    """Start a replay session."""
    try:
        # Find content entry
        if content_type not in content_storage:
            raise HTTPException(status_code=404, detail="Content type not found")
        
        entry = content_storage[content_type].get(content_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Create replay session
        session = ReplaySession(entry, narrator_role)
        replay_sessions[session.session_id] = session
        
        # Increment replay count
        entry.replay_count += 1
        save_content_entry(entry)
        
        return {
            "success": True,
            "session_id": session.session_id,
            "content": entry.to_dict(),
            "narration": session.narration_log
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/replay/{session_id}/narrate")
async def api_add_narration(
    session_id: str,
    message: str = Form(...),
    script_type: str = Form("guidance")
):
    """Add narration to a replay session."""
    try:
        session = replay_sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Replay session not found")
        
        if not session.is_active:
            raise HTTPException(status_code=400, detail="Replay session is not active")
        
        success = session.add_narration(message, script_type)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add narration")
        
        return {
            "success": True,
            "narration": session.narration_log[-1]  # Return the latest narration entry
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dispatch/again")
async def api_dispatch_again(
    content_type: str = Form(...),
    content_id: str = Form(...),
    dispatch_role: str = Form("herald"),
    custodian_name: str = Form("Archive System")
):
    """Dispatch content again with new ceremonial bindings."""
    try:
        # Find original content
        if content_type not in content_storage:
            raise HTTPException(status_code=404, detail="Content type not found")
        
        original_entry = content_storage[content_type].get(content_id)
        if not original_entry:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Create new content entry for redispatch
        dispatch_entry = ContentEntry(
            content_type=content_type,
            title=f"[REDISPATCH] {original_entry.title}",
            content=original_entry.content,
            role=dispatch_role,
            custodian_name=custodian_name
        )
        
        # Add dispatch metadata
        dispatch_entry.metadata.update({
            "original_id": original_entry.id,
            "original_binding": original_entry.sacred_binding,
            "dispatch_timestamp": datetime.now().isoformat(),
            "dispatch_reason": "ceremonial_redispatch"
        })
        
        # Store the new dispatch
        content_storage[content_type][dispatch_entry.id] = dispatch_entry
        save_content_entry(dispatch_entry)
        
        # Increment original dispatch count
        original_entry.dispatch_count += 1
        save_content_entry(original_entry)
        
        return {
            "success": True,
            "dispatch_id": dispatch_entry.id,
            "new_sacred_binding": dispatch_entry.sacred_binding,
            "dispatch_count": original_entry.dispatch_count,
            "sigil_verification": dispatch_entry.get_sigil_verification() if SIGIL_SYSTEM_AVAILABLE else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def api_get_stats():
    """Get archive statistics."""
    try:
        total_content = sum(len(storage) for storage in content_storage.values())
        total_replays = sum(entry.replay_count for storage in content_storage.values() for entry in storage.values())
        total_dispatches = sum(entry.dispatch_count for storage in content_storage.values() for entry in storage.values())
        
        content_by_type = {
            content_type: len(storage) 
            for content_type, storage in content_storage.items()
        }
        
        # SIGIL seal statistics
        sigil_stats = {}
        if SIGIL_SYSTEM_AVAILABLE and sigil_registry:
            try:
                sigil_stats = sigil_registry.get_registry_stats()
            except Exception as e:
                sigil_stats = {"error": f"Could not get SIGIL stats: {e}"}
        
        return {
            "success": True,
            "stats": {
                "total_content": total_content,
                "total_replays": total_replays,
                "total_dispatches": total_dispatches,
                "content_by_type": content_by_type,
                "avatar_system_status": "active" if AVATAR_SYSTEM_AVAILABLE else "unavailable",
                "sigil_system_status": "active" if SIGIL_SYSTEM_AVAILABLE else "unavailable",
                "sigil_seals": sigil_stats
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)