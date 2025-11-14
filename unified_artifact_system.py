"""
Unified Artifact Management System
==================================

A comprehensive system for managing all types of sacred artifacts:
- Hymns (Concord Hymn System)
- Charters (Final Eternal Charter)
- Decrees, Manifestos, and other artifacts
- With SIGIL seal authentication and multi-route support
"""

import json
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our SIGIL system
try:
    from sigil_seal_system import SIGILSeal, SealAuthority, CycleType, SealRegistry
except ImportError:
    print("Warning: SIGIL seal system not available. Running in standalone mode.")
    SIGILSeal = None

class ArtifactType(Enum):
    """Types of sacred artifacts"""
    HYMN = "hymn"
    CHARTER = "charter"
    DECREE = "decree"
    MANIFESTO = "manifesto"
    PROCLAMATION = "proclamation"
    COVENANT = "covenant"

class ArtifactCycle(Enum):
    """Artifact cycles"""
    DAILY = "daily"
    SEASONAL = "seasonal"
    EPOCHAL = "epochal"
    MILLENNIAL = "millennial"

class ArtifactAudience(Enum):
    """Authorized artifact audiences"""
    HEIRS = "heirs"
    COUNCILS = "councils"
    INSTITUTIONS = "institutions"
    CUSTODIANS = "custodians"
    PUBLIC = "public"

@dataclass
class ArtifactAssets:
    """Artifact multimedia assets"""
    text: str
    audio: Optional[str] = None
    glyph: Optional[str] = None
    background: Optional[str] = None

@dataclass
class ArtifactSigning:
    """Artifact signing information"""
    sigil: str
    signedBy: str
    heirsChorus: bool = False
    timestamp: Optional[str] = None

@dataclass
class ArtifactMetadata:
    """Additional artifact metadata"""
    createdAt: str
    classification: str
    authority: str
    bindingStrength: int
    realm: str
    seal: str

@dataclass
class ArtifactManifest:
    """Complete artifact manifest structure"""
    artifactId: str
    title: str
    version: str
    type: str
    routes: Dict[str, str]
    audience: List[str]
    cycles: List[str]
    files: Dict[str, str]
    signing: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Artifact:
    """Sacred artifact with all properties"""
    manifest: ArtifactManifest
    assets: ArtifactAssets
    signing: ArtifactSigning
    metadata: ArtifactMetadata
    performances: List[Dict[str, Any]]
    sigil_seal: Optional[str] = None
    registered_at: Optional[str] = None

class UnifiedArtifactSystem:
    """Unified system for managing all sacred artifacts"""
    
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        self.sigil_registry = SealRegistry() if SIGILSeal else None
        self.startup_timestamp = datetime.now(timezone.utc).isoformat()
        
        # Load any existing artifacts
        self._load_existing_artifacts()
    
    def _load_existing_artifacts(self):
        """Load existing artifacts from storage"""
        artifacts_file = Path("artifacts_registry.json")
        if artifacts_file.exists():
            try:
                with open(artifacts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for artifact_id, artifact_data in data.items():
                        # Reconstruct artifact objects
                        manifest = ArtifactManifest(**artifact_data['manifest'])
                        assets = ArtifactAssets(**artifact_data['assets'])
                        signing = ArtifactSigning(**artifact_data['signing'])
                        metadata = ArtifactMetadata(**artifact_data['metadata'])
                        
                        artifact = Artifact(
                            manifest=manifest,
                            assets=assets,
                            signing=signing,
                            metadata=metadata,
                            performances=artifact_data.get('performances', []),
                            sigil_seal=artifact_data.get('sigil_seal'),
                            registered_at=artifact_data.get('registered_at')
                        )
                        self.artifacts[artifact_id] = artifact
                        print(f"✅ Loaded artifact: {artifact_id}")
            except Exception as e:
                print(f"Warning: Could not load artifacts registry: {e}")
    
    def _save_artifacts(self):
        """Save artifacts to persistent storage"""
        artifacts_file = Path("artifacts_registry.json")
        try:
            serializable_data = {}
            for artifact_id, artifact in self.artifacts.items():
                serializable_data[artifact_id] = {
                    'manifest': asdict(artifact.manifest),
                    'assets': asdict(artifact.assets),
                    'signing': asdict(artifact.signing),
                    'metadata': asdict(artifact.metadata),
                    'performances': artifact.performances,
                    'sigil_seal': artifact.sigil_seal,
                    'registered_at': artifact.registered_at
                }
            
            with open(artifacts_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Warning: Could not save artifacts registry: {e}")
    
    def register_artifact(self, manifest_data: dict, text_content: str, glyph_content: str = None) -> dict:
        """Register a new sacred artifact"""
        try:
            # Parse manifest
            manifest = ArtifactManifest(**manifest_data)
            
            # Create assets
            assets = ArtifactAssets(
                text=text_content,
                glyph=glyph_content
            )
            
            # Create signing info
            signing_data = manifest_data.get('signing', {})
            signing = ArtifactSigning(
                sigil=signing_data.get('sigil', f"SIGIL-{manifest.type.upper()}-{uuid.uuid4().hex[:8]}"),
                signedBy=signing_data.get('signedBy', 'Custodian'),
                heirsChorus=signing_data.get('heirsChorus', False),
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
            # Create metadata
            metadata_data = manifest_data.get('metadata', {})
            metadata = ArtifactMetadata(
                createdAt=metadata_data.get('createdAt', datetime.now(timezone.utc).isoformat()),
                classification=metadata_data.get('classification', 'Sacred Artifact'),
                authority=metadata_data.get('authority', 'Supreme'),
                bindingStrength=metadata_data.get('bindingStrength', 100),
                realm=metadata_data.get('realm', 'Codex Dominion'),
                seal=metadata_data.get('seal', f"{manifest.type.title()} Seal")
            )
            
            # Create SIGIL seal if system available
            sigil_seal = None
            if self.sigil_registry and SIGILSeal:
                try:
                    seal = SIGILSeal(
                        identifier=f"{manifest.type}-{manifest.artifactId}",
                        authority=SealAuthority.SUPREME,
                        binding_strength=metadata.bindingStrength,
                        created_by="Custodian-Heirs System"
                    )
                    sigil_seal = seal.seal_code
                    self.sigil_registry.register_seal(seal)
                except Exception as e:
                    print(f"Warning: Could not create SIGIL seal: {e}")
            
            # Create complete artifact
            artifact = Artifact(
                manifest=manifest,
                assets=assets,
                signing=signing,
                metadata=metadata,
                performances=[],
                sigil_seal=sigil_seal,
                registered_at=datetime.now(timezone.utc).isoformat()
            )
            
            # Register artifact
            self.artifacts[manifest.artifactId] = artifact
            self._save_artifacts()
            
            return {
                "status": "success",
                "artifactId": manifest.artifactId,
                "title": manifest.title,
                "type": manifest.type,
                "sigil": signing.sigil,
                "sigilSeal": sigil_seal,
                "authority": metadata.authority,
                "bindingStrength": metadata.bindingStrength,
                "registeredAt": artifact.registered_at
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to register artifact: {str(e)}")
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID"""
        return self.artifacts.get(artifact_id)
    
    def list_artifacts(self) -> dict:
        """List all registered artifacts"""
        artifacts_list = []
        for artifact_id, artifact in self.artifacts.items():
            artifacts_list.append({
                "artifactId": artifact_id,
                "title": artifact.manifest.title,
                "type": artifact.manifest.type,
                "version": artifact.manifest.version,
                "audience": artifact.manifest.audience,
                "cycles": artifact.manifest.cycles,
                "performances": len(artifact.performances),
                "sigilProtected": bool(artifact.sigil_seal),
                "authority": artifact.metadata.authority,
                "registeredAt": artifact.registered_at
            })
        
        return {
            "system": "Unified Artifact Management System",
            "version": "1.0.0",
            "totalArtifacts": len(artifacts_list),
            "sigilSystem": bool(self.sigil_registry),
            "artifacts": artifacts_list
        }
    
    def record_performance(self, artifact_id: str, with_heirs: bool = False) -> dict:
        """Record a performance/activation of an artifact"""
        if artifact_id not in self.artifacts:
            raise HTTPException(status_code=404, detail="Artifact not found")
        
        performance = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "withHeirsChorus": with_heirs,
            "performer": "heirs-chorus" if with_heirs else "custodian"
        }
        
        self.artifacts[artifact_id].performances.append(performance)
        self._save_artifacts()
        
        return {
            "status": "success",
            "artifactId": artifact_id,
            "performance": performance,
            "totalPerformances": len(self.artifacts[artifact_id].performances)
        }

# Initialize the unified system
artifact_system = UnifiedArtifactSystem()

# Create FastAPI app
app = FastAPI(
    title="Unified Artifact Management System",
    description="Sacred artifact management with hymns, charters, and SIGIL authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """System status and overview"""
    return artifact_system.list_artifacts()

@app.post("/ledger/continuum/hymn")
async def register_hymn(manifest: str = Form(), text_content: str = Form(), glyph_content: Optional[str] = Form(None)):
    """Register a sacred hymn (backward compatibility)"""
    # Parse manifest from JSON string
    try:
        manifest_data = json.loads(manifest)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid manifest JSON")
    
    # Ensure type is hymn
    manifest_data['type'] = 'hymn'
    return artifact_system.register_artifact(manifest_data, text_content, glyph_content)

@app.post("/ledger/charter/final")
async def register_charter(manifest: str = Form(), text_content: str = Form(), glyph_content: Optional[str] = Form(None)):
    """Register a sacred charter"""
    # Parse manifest from JSON string
    try:
        manifest_data = json.loads(manifest)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid manifest JSON")
    
    # Ensure type is charter
    manifest_data['type'] = 'charter'
    return artifact_system.register_artifact(manifest_data, text_content, glyph_content)

@app.post("/ledger/artifact/generic")
async def register_artifact(manifest: str = Form(), text_content: str = Form(), glyph_content: Optional[str] = Form(None)):
    """Register any type of sacred artifact"""
    # Parse manifest from JSON string
    try:
        manifest_data = json.loads(manifest)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid manifest JSON")
    
    return artifact_system.register_artifact(manifest_data, text_content, glyph_content)

@app.post("/upload/artifact")
async def upload_artifact_files(
    artifactId: str = Form(), 
    version: str = Form(), 
    files: Optional[List[UploadFile]] = File(None),
    text: Optional[UploadFile] = File(None),
    glyph: Optional[UploadFile] = File(None)
):
    """Upload artifact files (flexible file handling)"""
    uploaded_files = []
    
    # Handle both list of files and individual file parameters
    all_files = []
    if files:
        all_files.extend(files)
    if text:
        all_files.append(text)
    if glyph:
        all_files.append(glyph)
    
    for file in all_files:
        if file:
            content = await file.read()
            uploaded_files.append({
                "filename": file.filename,
                "size": len(content),
                "content_type": file.content_type
            })
    
    return {
        "status": "uploaded",
        "artifactId": artifactId,
        "version": version,
        "files": uploaded_files,
        "totalFiles": len(uploaded_files)
    }

@app.post("/dispatch/global")
async def dispatch_artifact(artifact_id: str, dispatch_to: List[str] = ["all-realms"]):
    """Dispatch artifact globally across all realms"""
    artifact = artifact_system.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    # Record as a special performance
    dispatch_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "global_dispatch",
        "dispatchTo": dispatch_to,
        "performer": "custodian-system"
    }
    
    artifact.performances.append(dispatch_record)
    artifact_system._save_artifacts()
    
    return {
        "status": "dispatched",
        "artifactId": artifact_id,
        "title": artifact.manifest.title,
        "dispatchTo": dispatch_to,
        "timestamp": dispatch_record["timestamp"]
    }

@app.get("/replay/charter")
async def replay_charter(artifact_id: Optional[str] = None):
    """Replay charter ceremonies"""
    if artifact_id:
        artifact = artifact_system.get_artifact(artifact_id)
        if not artifact:
            raise HTTPException(status_code=404, detail="Charter not found")
        
        return {
            "artifactId": artifact_id,
            "title": artifact.manifest.title,
            "type": artifact.manifest.type,
            "performances": artifact.performances,
            "totalPerformances": len(artifact.performances)
        }
    else:
        # Return all charter replays
        charters = {k: v for k, v in artifact_system.artifacts.items() 
                   if v.manifest.type == 'charter'}
        
        return {
            "totalCharters": len(charters),
            "charters": {k: {
                "title": v.manifest.title,
                "performances": len(v.performances)
            } for k, v in charters.items()}
        }

@app.post("/artifacts/{artifact_id}/perform")
async def perform_artifact(artifact_id: str, with_heirs: bool = False):
    """Record a performance/activation of an artifact"""
    return artifact_system.record_performance(artifact_id, with_heirs)

@app.get("/artifacts/list")
async def list_artifacts():
    """List all registered artifacts"""
    return artifact_system.list_artifacts()

@app.get("/artifacts/{artifact_id}")
async def get_artifact(artifact_id: str):
    """Get detailed artifact information"""
    artifact = artifact_system.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    return {
        "artifactId": artifact_id,
        "manifest": asdict(artifact.manifest),
        "signing": asdict(artifact.signing),
        "metadata": asdict(artifact.metadata),
        "performances": artifact.performances,
        "sigilSeal": artifact.sigil_seal,
        "registeredAt": artifact.registered_at,
        "textPreview": artifact.assets.text[:500] + "..." if len(artifact.assets.text) > 500 else artifact.assets.text
    }

@app.get("/ledger/charter/final/{artifact_id}")
async def get_charter_ledger(artifact_id: str):
    """Get charter ledger entries"""
    artifact = artifact_system.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Charter not found")
    
    return {
        "artifactId": artifact_id,
        "ledgerEntries": artifact.performances,
        "count": len(artifact.performances),
        "title": artifact.manifest.title,
        "type": artifact.manifest.type,
        "registeredAt": artifact.registered_at
    }

@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "operational",
        "system": "Unified Artifact Management System",
        "version": "1.0.0",
        "artifacts": len(artifact_system.artifacts),
        "sigilSystem": bool(artifact_system.sigil_registry),
        "uptime": datetime.now(timezone.utc).isoformat()
    }

# Demo function for testing
def demo_unified_system():
    """Run a demonstration of the unified artifact system"""
    print("\n" + "="*60)
    print("🌟 UNIFIED ARTIFACT MANAGEMENT SYSTEM DEMO 🌟")
    print("="*60)
    
    # Demo artifact registration
    demo_charter_manifest = {
        "artifactId": "demo-eternal-charter",
        "title": "Demo Eternal Charter",
        "version": "1.0.0",
        "type": "charter",
        "routes": {
            "register": "/ledger/charter/final",
            "dispatch": "/dispatch/global",
            "replay": "/replay/charter"
        },
        "audience": ["heirs", "councils", "custodians", "public"],
        "cycles": ["epochal", "millennial"],
        "files": {
            "text": "charter.md",
            "glyph": "assets/flame_glyph.svg"
        },
        "signing": {
            "sigil": "SIGIL-DEMO-CHARTER-001",
            "signedBy": "Custodian",
            "heirsChorus": True
        }
    }
    
    demo_charter_text = "# Demo Eternal Charter\nThis is a demonstration charter for testing the unified artifact system."
    
    print("1. 📜 Registering Demo Charter")
    result = artifact_system.register_artifact(demo_charter_manifest, demo_charter_text)
    print(f"   ✅ Charter registered: {result['artifactId']}")
    print(f"   🔥 SIGIL: {result['sigil']}")
    print(f"   👑 Authority: {result['authority']} (Strength: {result['bindingStrength']})")
    
    print("\n2. 🔄 Recording Performances")
    artifact_system.record_performance(result['artifactId'], with_heirs=True)
    artifact_system.record_performance(result['artifactId'], with_heirs=False)
    print(f"   🎭 Performances recorded for {result['artifactId']}")
    
    print("\n3. 📊 System Statistics")
    stats = artifact_system.list_artifacts()
    print(f"   📚 Total Artifacts: {stats['totalArtifacts']}")
    print(f"   🔐 SIGIL System: {'Active' if stats['sigilSystem'] else 'Inactive'}")
    
    for artifact in stats['artifacts']:
        print(f"   📋 {artifact['title']} ({artifact['type']}) - {artifact['performances']} performances")
    
    print("\n✨ Unified Artifact System Demo Complete! ✨")
    print("="*60)

if __name__ == "__main__":
    # Run demo
    demo_unified_system()
    
    print("\n🌐 Starting Unified Artifact Web Server...")
    print("🎯 Access at: http://localhost:8004")
    print("📖 API Docs: http://localhost:8004/docs")
    print("🔍 Health Check: http://localhost:8004/health")
    
    # Start the web server
    uvicorn.run(app, host="0.0.0.0", port=8004)