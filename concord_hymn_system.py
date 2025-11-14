"""
Custodian–Heirs Concord Hymn System
===================================

A comprehensive system for managing sacred hymns with SIGIL seal authentication,
multi-cycle support, and heirs chorus functionality.
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Import our SIGIL system
try:
    from sigil_seal_system import SIGILSeal, SealAuthority, CycleType, SealRegistry
except ImportError:
    print("Warning: SIGIL seal system not available. Running in standalone mode.")
    SIGILSeal = None

class HymnCycle(Enum):
    """Hymn recitation cycles"""
    DAILY = "daily"
    SEASONAL = "seasonal" 
    EPOCHAL = "epochal"
    MILLENNIAL = "millennial"

class HymnAudience(Enum):
    """Authorized hymn audiences"""
    HEIRS = "heirs"
    COUNCILS = "councils"
    INSTITUTIONS = "institutions"
    CUSTODIANS = "custodians"

@dataclass
class HymnAssets:
    """Hymn multimedia assets"""
    text: str
    audio: Optional[str] = None
    glyph: Optional[str] = None
    background: Optional[str] = None

@dataclass
class HymnSigning:
    """Hymn SIGIL signing information"""
    sigil: str
    signed_by: str
    heirs_chorus: bool = False
    seal_object: Optional[Dict] = None

@dataclass
class ConcordHymn:
    """Main hymn data structure"""
    artifact_id: str
    title: str
    version: str
    type: str = "hymn"
    routes: Dict[str, str] = None
    audience: List[str] = None
    cycles: List[str] = None
    files: HymnAssets = None
    hash_strategy: str = "sha256"
    signing: HymnSigning = None
    created_at: datetime = None
    last_performed: Optional[datetime] = None
    performance_count: int = 0
    heirs_chorus_count: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.routes is None:
            self.routes = {
                "register": "/ledger/continuum/hymn",
                "dispatch": "/dispatch/global", 
                "replay": "/replay/cycles"
            }
        if self.audience is None:
            self.audience = ["heirs", "councils", "institutions", "custodians"]
        if self.cycles is None:
            self.cycles = ["daily", "seasonal", "epochal", "millennial"]

    def generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash of hymn content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def create_sigil_seal(self, content: str) -> Optional[Dict]:
        """Create SIGIL seal for hymn authentication"""
        if not SIGILSeal:
            return None
        
        # Map signing authority
        authority_map = {
            "Custodian": SealAuthority.SUPREME,
            "Council": SealAuthority.HIGH, 
            "Institution": SealAuthority.SACRED,
            "Heir": SealAuthority.GUARDIAN
        }
        
        authority = authority_map.get(self.signing.signed_by, SealAuthority.INITIATE)
        
        # Create seal with hymn-specific metadata
        seal = SIGILSeal(
            custodian_name=self.signing.signed_by,
            avatar_role="Hymn Custodian",
            cycle_tag=self.artifact_id,
            content_hash=self.generate_content_hash(content),
            authority=authority,
            cycle_type=CycleType.ETERNAL  # Hymns are eternal
        )
        
        self.signing.seal_object = {
            "seal_id": seal.seal_id,
            "custodian_name": seal.custodian_name,
            "avatar_role": seal.avatar_role,
            "content_hash": seal.content_hash,
            "authority": seal.authority.value,
            "binding_strength": seal.binding_strength,
            "flame_glyph": seal.generate_flame_glyph(),
            "binding_sigil": seal.generate_binding_sigil(),
            "created_at": seal.issued_at.isoformat(),
            "cycle_tag": seal.cycle_tag,
            "cycle_type": seal.cycle_type.value,
            "metadata": {
                "hymn_id": self.artifact_id,
                "hymn_title": self.title,
                "hymn_version": self.version,
                "heirs_chorus": self.signing.heirs_chorus,
                "audience": self.audience,
                "cycles": self.cycles
            }
        }
        
        return self.signing.seal_object

    def record_performance(self, with_heirs_chorus: bool = False):
        """Record a hymn performance"""
        self.last_performed = datetime.now(timezone.utc)
        self.performance_count += 1
        if with_heirs_chorus:
            self.heirs_chorus_count += 1

class HymnRegistry:
    """Registry for managing all hymns"""
    
    def __init__(self, registry_file: str = "hymn_registry.json"):
        self.registry_file = Path(registry_file)
        self.hymns: Dict[str, ConcordHymn] = {}
        self.sigil_registry = None
        if SIGILSeal:
            self.sigil_registry = SealRegistry("hymn_seals.json")
        self.load_registry()

    def load_registry(self):
        """Load hymns from registry file"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for hymn_id, hymn_data in data.items():
                        # Convert datetime strings back to datetime objects
                        if 'created_at' in hymn_data:
                            hymn_data['created_at'] = datetime.fromisoformat(hymn_data['created_at'])
                        if 'last_performed' in hymn_data and hymn_data['last_performed']:
                            hymn_data['last_performed'] = datetime.fromisoformat(hymn_data['last_performed'])
                        
                        # Reconstruct objects
                        if 'files' in hymn_data:
                            hymn_data['files'] = HymnAssets(**hymn_data['files'])
                        if 'signing' in hymn_data:
                            hymn_data['signing'] = HymnSigning(**hymn_data['signing'])
                        
                        self.hymns[hymn_id] = ConcordHymn(**hymn_data)
            except Exception as e:
                print(f"Warning: Could not load hymn registry: {e}")

    def save_registry(self):
        """Save hymns to registry file"""
        try:
            # Convert to serializable format
            data = {}
            for hymn_id, hymn in self.hymns.items():
                hymn_dict = asdict(hymn)
                # Convert datetime objects to strings
                if hymn_dict['created_at']:
                    hymn_dict['created_at'] = hymn.created_at.isoformat()
                if hymn_dict['last_performed']:
                    hymn_dict['last_performed'] = hymn.last_performed.isoformat()
                data[hymn_id] = hymn_dict
            
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving hymn registry: {e}")

    def register_hymn(self, hymn_spec: Dict) -> ConcordHymn:
        """Register a new hymn from specification"""
        # Create assets object
        files = HymnAssets(**hymn_spec.get('files', {}))
        
        # Create signing object
        signing_data = hymn_spec.get('signing', {})
        signing = HymnSigning(**signing_data)
        
        # Create main hymn object
        hymn = ConcordHymn(
            artifact_id=hymn_spec['artifactId'],
            title=hymn_spec['title'],
            version=hymn_spec['version'],
            type=hymn_spec.get('type', 'hymn'),
            routes=hymn_spec.get('routes'),
            audience=hymn_spec.get('audience'),
            cycles=hymn_spec.get('cycles'),
            files=files,
            hash_strategy=hymn_spec.get('hashStrategy', 'sha256'),
            signing=signing
        )
        
        # Load hymn content and create SIGIL seal
        content = self.load_hymn_content(files.text)
        if content and signing:
            seal = hymn.create_sigil_seal(content)
            
            # Register seal if SIGIL system available
            if self.sigil_registry and hymn.signing.seal_object:
                try:
                    # Find the actual seal object (we need to recreate it for registration)
                    # For now, just log success without registry storage
                    print(f"SIGIL seal created for hymn: {hymn.artifact_id}")
                except Exception as e:
                    print(f"Warning: Could not register SIGIL seal: {e}")
        
        self.hymns[hymn.artifact_id] = hymn
        self.save_registry()
        return hymn

    def load_hymn_content(self, text_file: str) -> Optional[str]:
        """Load hymn text content from file"""
        try:
            file_path = Path(text_file)
            if file_path.exists():
                return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not load hymn content from {text_file}: {e}")
        return None

    def get_hymn(self, artifact_id: str) -> Optional[ConcordHymn]:
        """Retrieve hymn by ID"""
        return self.hymns.get(artifact_id)

    def list_hymns(self) -> List[Dict]:
        """List all registered hymns"""
        hymn_list = []
        for hymn in self.hymns.values():
            hymn_list.append({
                "artifact_id": hymn.artifact_id,
                "title": hymn.title,
                "version": hymn.version,
                "audience": hymn.audience,
                "cycles": hymn.cycles,
                "performance_count": hymn.performance_count,
                "heirs_chorus_count": hymn.heirs_chorus_count,
                "last_performed": hymn.last_performed.isoformat() if hymn.last_performed else None,
                "has_sigil": hymn.signing.seal_object is not None if hymn.signing else False
            })
        return hymn_list

    def perform_hymn(self, artifact_id: str, with_heirs_chorus: bool = False) -> Dict:
        """Record a hymn performance"""
        hymn = self.get_hymn(artifact_id)
        if not hymn:
            raise ValueError(f"Hymn {artifact_id} not found")
        
        hymn.record_performance(with_heirs_chorus)
        self.save_registry()
        
        return {
            "hymn_id": artifact_id,
            "title": hymn.title,
            "performance_time": hymn.last_performed.isoformat(),
            "total_performances": hymn.performance_count,
            "heirs_chorus": with_heirs_chorus,
            "heirs_chorus_total": hymn.heirs_chorus_count
        }

    def get_hymns_by_cycle(self, cycle: str) -> List[ConcordHymn]:
        """Get hymns suitable for a specific cycle"""
        return [hymn for hymn in self.hymns.values() if cycle in hymn.cycles]

    def get_hymns_by_audience(self, audience: str) -> List[ConcordHymn]:
        """Get hymns for a specific audience"""
        return [hymn for hymn in self.hymns.values() if audience in hymn.audience]

    def verify_hymn_seal(self, artifact_id: str) -> Dict:
        """Verify SIGIL seal for a hymn"""
        hymn = self.get_hymn(artifact_id)
        if not hymn or not hymn.signing or not hymn.signing.seal_object:
            return {"verified": False, "reason": "No seal found"}
        
        if not SIGILSeal:
            return {"verified": False, "reason": "SIGIL system unavailable"}
        
        try:
            # Load current content and verify hash
            content = self.load_hymn_content(hymn.files.text)
            if not content:
                return {"verified": False, "reason": "Content not found"}
            
            current_hash = hymn.generate_content_hash(content)
            stored_hash = hymn.signing.seal_object['content_hash']
            
            if current_hash != stored_hash:
                return {
                    "verified": False, 
                    "reason": "Content hash mismatch",
                    "current_hash": current_hash,
                    "stored_hash": stored_hash
                }
            
            return {
                "verified": True,
                "seal_id": hymn.signing.seal_object['seal_id'],
                "authority": hymn.signing.seal_object['authority'],
                "binding_strength": hymn.signing.seal_object['binding_strength'],
                "flame_glyph": hymn.signing.seal_object['flame_glyph'],
                "signed_by": hymn.signing.signed_by,
                "created_at": hymn.signing.seal_object['created_at']
            }
            
        except Exception as e:
            return {"verified": False, "reason": f"Verification error: {str(e)}"}

# Initialize global registry
hymn_registry = HymnRegistry()

# FastAPI Application
app = FastAPI(title="Custodian–Heirs Concord Hymn System", version="1.0.0")

# Create assets directory
assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Create templates directory  
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

# Mount static assets
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Setup templates (for future use)
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    """Root endpoint with system status"""
    return {
        "system": "Custodian–Heirs Concord Hymn System",
        "version": "1.0.0",
        "hymns_registered": len(hymn_registry.hymns),
        "sigil_system": SIGILSeal is not None,
        "routes": {
            "register": "/ledger/continuum/hymn",
            "dispatch": "/dispatch/global",
            "replay": "/replay/cycles",
            "list": "/hymns/list",
            "performance": "/hymns/{hymn_id}/perform"
        }
    }

@app.post("/ledger/continuum/hymn")
async def register_hymn(hymn_spec: Dict):
    """Register a new hymn in the continuum ledger"""
    try:
        hymn = hymn_registry.register_hymn(hymn_spec)
        return {
            "success": True,
            "hymn_id": hymn.artifact_id,
            "title": hymn.title,
            "version": hymn.version,
            "seal_created": hymn.signing.seal_object is not None if hymn.signing else False,
            "registered_at": hymn.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.get("/dispatch/global")
async def global_dispatch():
    """Global hymn dispatch system"""
    return {
        "dispatch_type": "global",
        "available_hymns": hymn_registry.list_hymns(),
        "total_hymns": len(hymn_registry.hymns),
        "dispatch_time": datetime.now(timezone.utc).isoformat()
    }

@app.get("/replay/cycles")
async def replay_cycles():
    """Hymn cycle replay system"""
    cycles_data = {}
    for cycle in HymnCycle:
        cycle_hymns = hymn_registry.get_hymns_by_cycle(cycle.value)
        cycles_data[cycle.value] = {
            "count": len(cycle_hymns),
            "hymns": [{"id": h.artifact_id, "title": h.title} for h in cycle_hymns]
        }
    
    return {
        "replay_type": "cycles",
        "cycles": cycles_data,
        "replay_time": datetime.now(timezone.utc).isoformat()
    }

@app.get("/hymns/list")
async def list_hymns():
    """List all registered hymns"""
    return {
        "hymns": hymn_registry.list_hymns(),
        "total": len(hymn_registry.hymns)
    }

@app.get("/hymns/{hymn_id}")
async def get_hymn_details(hymn_id: str):
    """Get detailed hymn information"""
    hymn = hymn_registry.get_hymn(hymn_id)
    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")
    
    # Load content
    content = hymn_registry.load_hymn_content(hymn.files.text) if hymn.files else None
    
    return {
        "hymn": {
            "artifact_id": hymn.artifact_id,
            "title": hymn.title,
            "version": hymn.version,
            "type": hymn.type,
            "audience": hymn.audience,
            "cycles": hymn.cycles,
            "performance_count": hymn.performance_count,
            "heirs_chorus_count": hymn.heirs_chorus_count,
            "last_performed": hymn.last_performed.isoformat() if hymn.last_performed else None,
            "created_at": hymn.created_at.isoformat()
        },
        "content": content,
        "seal_verification": hymn_registry.verify_hymn_seal(hymn_id)
    }

@app.post("/hymns/{hymn_id}/perform")
async def perform_hymn(hymn_id: str, heirs_chorus: bool = False):
    """Record a hymn performance"""
    try:
        performance = hymn_registry.perform_hymn(hymn_id, heirs_chorus)
        return {
            "success": True,
            "performance": performance
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance recording failed: {str(e)}")

@app.get("/hymns/{hymn_id}/verify")
async def verify_hymn_seal(hymn_id: str):
    """Verify SIGIL seal for a hymn"""
    verification = hymn_registry.verify_hymn_seal(hymn_id)
    return verification

@app.get("/interface", response_class=HTMLResponse)
async def hymn_interface():
    """Web interface for the Concord Hymn System"""
    try:
        interface_file = Path("templates/concord_hymn_interface.html")
        if interface_file.exists():
            return interface_file.read_text(encoding='utf-8')
        else:
            return HTMLResponse(content="""
            <html>
                <head><title>Concord Hymn System</title></head>
                <body>
                    <h1>Custodian–Heirs Concord Hymn System</h1>
                    <p>Interface template not found. Please ensure concord_hymn_interface.html exists in templates/</p>
                    <a href="/docs">View API Documentation</a>
                </body>
            </html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>")

@app.get("/cycles/{cycle}/hymns")
async def get_hymns_by_cycle(cycle: str):
    """Get hymns for a specific cycle"""
    try:
        cycle_enum = HymnCycle(cycle)
        hymns = hymn_registry.get_hymns_by_cycle(cycle)
        return {
            "cycle": cycle,
            "hymns": [{"id": h.artifact_id, "title": h.title, "version": h.version} for h in hymns],
            "count": len(hymns)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid cycle: {cycle}")

@app.get("/audience/{audience}/hymns") 
async def get_hymns_by_audience(audience: str):
    """Get hymns for a specific audience"""
    try:
        audience_enum = HymnAudience(audience)
        hymns = hymn_registry.get_hymns_by_audience(audience)
        return {
            "audience": audience,
            "hymns": [{"id": h.artifact_id, "title": h.title, "version": h.version} for h in hymns],
            "count": len(hymns)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid audience: {audience}")

def demo_concord_hymn_system():
    """Demonstration of the Concord Hymn system"""
    print("\n" + "="*60)
    print("🎵 CUSTODIAN–HEIRS CONCORD HYMN SYSTEM DEMO 🎵")
    print("="*60)
    
    # Create the specification from the user's request
    hymn_spec = {
        "artifactId": "codex-dominion-concord-hymn",
        "title": "Custodian–Heirs Concord Hymn",
        "version": "1.0.0",
        "type": "hymn",
        "routes": {
            "register": "/ledger/continuum/hymn",
            "dispatch": "/dispatch/global",
            "replay": "/replay/cycles"
        },
        "audience": ["heirs", "councils", "institutions", "custodians"],
        "cycles": ["daily", "seasonal", "epochal", "millennial"],
        "files": {
            "text": "concord_hymn.md",
            "audio": "assets/concord_theme.mp3",
            "glyph": "assets/flame_glyph.svg",
            "background": "assets/chorus_bg.png"
        },
        "hashStrategy": "sha256",
        "signing": {
            "sigil": "SIGIL-CONCORD-001",
            "signed_by": "Custodian",
            "heirs_chorus": True
        }
    }
    
    print(f"\n1. 📝 Registering Hymn: '{hymn_spec['title']}'")
    hymn = hymn_registry.register_hymn(hymn_spec)
    print(f"   ✅ Hymn registered with ID: {hymn.artifact_id}")
    
    if hymn.signing and hymn.signing.seal_object:
        seal = hymn.signing.seal_object
        print(f"   🔥 SIGIL Seal Created: {seal['flame_glyph']} {seal['binding_sigil']}")
        print(f"   🛡️  Authority: {seal['authority']} (Strength: {seal['binding_strength']})")
    
    print(f"\n2. 🎭 Recording Performances")
    # Regular performance
    perf1 = hymn_registry.perform_hymn(hymn.artifact_id, with_heirs_chorus=False)
    print(f"   🎪 Regular Performance: {perf1['performance_time']}")
    
    # Heirs chorus performance
    perf2 = hymn_registry.perform_hymn(hymn.artifact_id, with_heirs_chorus=True)
    print(f"   👥 Heirs Chorus Performance: {perf2['performance_time']}")
    print(f"   📊 Total: {perf2['total_performances']}, With Heirs: {perf2['heirs_chorus_total']}")
    
    print(f"\n3. 🔍 Verifying SIGIL Seal")
    verification = hymn_registry.verify_hymn_seal(hymn.artifact_id)
    if verification['verified']:
        print(f"   ✅ Seal Verified: {verification['flame_glyph']} (Authority: {verification['authority']})")
        print(f"   🔗 Binding Strength: {verification['binding_strength']}")
    else:
        print(f"   ❌ Verification Failed: {verification['reason']}")
    
    print(f"\n4. 📋 System Statistics")
    hymn_list = hymn_registry.list_hymns()
    print(f"   📚 Total Hymns: {len(hymn_list)}")
    for hymn_info in hymn_list:
        print(f"   🎵 {hymn_info['title']} v{hymn_info['version']}")
        print(f"      👥 Audiences: {', '.join(hymn_info['audience'])}")
        print(f"      🔄 Cycles: {', '.join(hymn_info['cycles'])}")
        print(f"      🎭 Performances: {hymn_info['performance_count']} (Heirs: {hymn_info['heirs_chorus_count']})")
        print(f"      🔐 SIGIL Protected: {'Yes' if hymn_info['has_sigil'] else 'No'}")
    
    print(f"\n5. 🌟 Cycle Analysis")
    for cycle in ["daily", "seasonal", "epochal", "millennial"]:
        cycle_hymns = hymn_registry.get_hymns_by_cycle(cycle)
        print(f"   {cycle.title()}: {len(cycle_hymns)} hymns")
    
    print(f"\n6. 👑 Audience Analysis") 
    for audience in ["heirs", "councils", "institutions", "custodians"]:
        audience_hymns = hymn_registry.get_hymns_by_audience(audience)
        print(f"   {audience.title()}: {len(audience_hymns)} hymns")
    
    print(f"\n✨ Concord Hymn System Demo Complete! ✨")
    print("="*60)

if __name__ == "__main__":
    # Run demonstration
    demo_concord_hymn_system()
    
    # Start web server
    print(f"\n🌐 Starting Concord Hymn Web Server...")
    print(f"🎵 Access at: http://localhost:8004")
    print(f"📖 API Docs: http://localhost:8004/docs")
    print(f"🖥️  Web Interface: http://localhost:8004/interface")
    
    uvicorn.run(app, host="0.0.0.0", port=8004)