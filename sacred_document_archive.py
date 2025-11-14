#!/usr/bin/env python3
"""
Sacred Document Archival System
FastAPI Integration for the Dominion

This module provides ceremonial document upload, storage, and archival
capabilities with sacred bindings and treasury integration.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
try:
    import aiofiles
except ImportError:
    print("⚠️  aiofiles not available - using synchronous file operations")
    aiofiles = None

try:
    import asyncpg
except ImportError:
    print("⚠️  asyncpg not available - PostgreSQL storage disabled")
    asyncpg = None

# Sacred ceremony imports
try:
    from treasury import CeremonialTreasury, ResourceType
except ImportError:
    print("⚠️  Treasury module not available - running in standalone mode")
    CeremonialTreasury = None
    ResourceType = None


class DocumentType(Enum):
    """Sacred document classifications"""
    CEREMONIAL_SCROLL = "ceremonial_scroll"
    SACRED_CONTRACT = "sacred_contract"
    FLAME_BLESSING = "flame_blessing"
    LITURGICAL_TEXT = "liturgical_text"
    TREASURY_RECORD = "treasury_record"
    COUNCIL_DECREE = "council_decree"
    WISDOM_CODEX = "wisdom_codex"
    HONOR_CITATION = "honor_citation"
    BINDING_OATH = "binding_oath"
    ARCHIVE_DOCUMENT = "archive_document"


class DocumentStatus(Enum):
    """Document processing states"""
    RECEIVED = "received"
    VALIDATING = "validating"
    ARCHIVED = "archived"
    BLESSED = "blessed"
    SEALED = "sealed"
    REJECTED = "rejected"
    CORRUPTED = "corrupted"


class SacredPriority(Enum):
    """Document priority classifications"""
    MUNDANE = "mundane"
    IMPORTANT = "important"
    SACRED = "sacred"
    DIVINE = "divine"
    ETERNAL = "eternal"


@dataclass
class SacredDocument:
    """Sacred document with ceremonial bindings"""
    document_id: str
    filename: str
    original_name: str
    file_size: int
    content_hash: str
    mime_type: str
    document_type: DocumentType
    priority: SacredPriority
    status: DocumentStatus
    upload_timestamp: str
    sacred_binding: str
    ceremonial_seal: str
    uploader_id: Optional[str]
    storage_path: str
    metadata: Dict[str, Any]
    treasury_cost: float
    flame_blessing: str
    archive_location: Optional[str] = None
    validation_errors: List[str] = None


class SacredDocumentArchive:
    """Sacred Document Archival System with ceremonial storage"""
    
    def __init__(self, storage_root: str = "./sacred_archives", 
                 postgres_url: str = None, treasury = None):
        self.storage_root = Path(storage_root)
        self.postgres_url = postgres_url
        self.treasury = treasury or (CeremonialTreasury() if CeremonialTreasury else None)
        
        # Initialize storage directories
        self._ensure_sacred_directories()
        
        # Document type costs (Sacred Tokens)
        self.archive_costs = {
            SacredPriority.MUNDANE: 0.01,
            SacredPriority.IMPORTANT: 0.05,
            SacredPriority.SACRED: 0.15,
            SacredPriority.DIVINE: 0.30,
            SacredPriority.ETERNAL: 1.00
        }
    
    def _ensure_sacred_directories(self):
        """Create sacred storage directory structure"""
        directories = [
            "documents",
            "documents/ceremonial_scrolls", 
            "documents/sacred_contracts",
            "documents/flame_blessings",
            "documents/liturgical_texts",
            "documents/treasury_records",
            "documents/council_decrees",
            "documents/wisdom_codices",
            "documents/honor_citations",
            "documents/binding_oaths",
            "documents/archive_documents",
            "metadata",
            "bindings",
            "sealed_archives"
        ]
        
        for directory in directories:
            (self.storage_root / directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_sacred_binding(self, document_data: Dict[str, Any]) -> str:
        """Generate sacred binding hash for document authenticity"""
        binding_elements = [
            document_data.get('filename', ''),
            document_data.get('content_hash', ''),
            document_data.get('upload_timestamp', ''),
            document_data.get('file_size', 0),
            "SACRED-DOMINION-BINDING"
        ]
        
        binding_string = '-'.join(str(elem) for elem in binding_elements)
        return hashlib.sha256(binding_string.encode()).hexdigest()[:32]
    
    def _generate_ceremonial_seal(self, document: SacredDocument) -> str:
        """Generate ceremonial seal for document verification"""
        seal_elements = [
            document.document_id,
            document.sacred_binding,
            document.priority.value,
            document.document_type.value,
            "ETERNAL-FLAME-SEAL"
        ]
        
        seal_string = '|'.join(seal_elements)
        return hashlib.sha256(seal_string.encode()).hexdigest()[:16].upper()
    
    def _generate_flame_blessing(self, document_type: DocumentType, priority: SacredPriority) -> str:
        """Generate contextual flame blessing for documents"""
        blessings = {
            (DocumentType.CEREMONIAL_SCROLL, SacredPriority.SACRED): "May the eternal flame preserve this sacred knowledge for all generations",
            (DocumentType.SACRED_CONTRACT, SacredPriority.DIVINE): "May the binding flame witness these solemn oaths and sacred agreements",
            (DocumentType.FLAME_BLESSING, SacredPriority.ETERNAL): "May the infinite flame multiply the blessings contained within",
            (DocumentType.LITURGICAL_TEXT, SacredPriority.SACRED): "May the sacred flame illuminate the hearts of all who read these words",
            (DocumentType.TREASURY_RECORD, SacredPriority.IMPORTANT): "May the watchful flame guard these precious resources",
            (DocumentType.COUNCIL_DECREE, SacredPriority.DIVINE): "May the sovereign flame guide the implementation of this decree",
            (DocumentType.WISDOM_CODEX, SacredPriority.ETERNAL): "May the ancient flame kindle wisdom in all who seek knowledge",
            (DocumentType.HONOR_CITATION, SacredPriority.SACRED): "May the glorious flame honor the deeds recorded herein",
            (DocumentType.BINDING_OATH, SacredPriority.DIVINE): "May the witnessing flame hold sacred all promises made",
            (DocumentType.ARCHIVE_DOCUMENT, SacredPriority.MUNDANE): "May the preserving flame keep this record for posterity"
        }
        
        return blessings.get((document_type, priority), "May the eternal flame bless this sacred archive")
    
    def _calculate_archive_cost(self, priority: SacredPriority, file_size: int) -> float:
        """Calculate ceremonial cost for document archival"""
        base_cost = self.archive_costs.get(priority, 0.01)
        
        # Size modifier (per MB)
        size_mb = file_size / (1024 * 1024)
        size_cost = size_mb * 0.001  # 0.001 Sacred Tokens per MB
        
        return round(base_cost + size_cost, 6)
    
    def _determine_document_type(self, filename: str, mime_type: str) -> DocumentType:
        """Determine document type from filename and MIME type"""
        filename_lower = filename.lower()
        
        # Document type detection patterns
        type_patterns = {
            DocumentType.CEREMONIAL_SCROLL: ['scroll', 'ceremony', 'ritual'],
            DocumentType.SACRED_CONTRACT: ['contract', 'agreement', 'pact'],
            DocumentType.FLAME_BLESSING: ['blessing', 'benediction', 'prayer'],
            DocumentType.LITURGICAL_TEXT: ['liturgy', 'service', 'worship'],
            DocumentType.TREASURY_RECORD: ['treasury', 'financial', 'budget'],
            DocumentType.COUNCIL_DECREE: ['decree', 'proclamation', 'edict'],
            DocumentType.WISDOM_CODEX: ['codex', 'knowledge', 'wisdom'],
            DocumentType.HONOR_CITATION: ['honor', 'citation', 'award'],
            DocumentType.BINDING_OATH: ['oath', 'vow', 'pledge']
        }
        
        for doc_type, patterns in type_patterns.items():
            if any(pattern in filename_lower for pattern in patterns):
                return doc_type
        
        return DocumentType.ARCHIVE_DOCUMENT
    
    def _determine_priority(self, document_type: DocumentType, file_size: int) -> SacredPriority:
        """Determine document priority based on type and characteristics"""
        # Priority based on document type
        type_priorities = {
            DocumentType.CEREMONIAL_SCROLL: SacredPriority.SACRED,
            DocumentType.SACRED_CONTRACT: SacredPriority.DIVINE,
            DocumentType.FLAME_BLESSING: SacredPriority.ETERNAL,
            DocumentType.LITURGICAL_TEXT: SacredPriority.SACRED,
            DocumentType.TREASURY_RECORD: SacredPriority.IMPORTANT,
            DocumentType.COUNCIL_DECREE: SacredPriority.DIVINE,
            DocumentType.WISDOM_CODEX: SacredPriority.ETERNAL,
            DocumentType.HONOR_CITATION: SacredPriority.SACRED,
            DocumentType.BINDING_OATH: SacredPriority.DIVINE,
            DocumentType.ARCHIVE_DOCUMENT: SacredPriority.MUNDANE
        }
        
        base_priority = type_priorities.get(document_type, SacredPriority.MUNDANE)
        
        # Adjust for large files (>10MB gets elevated)
        if file_size > 10 * 1024 * 1024:
            priority_elevation = {
                SacredPriority.MUNDANE: SacredPriority.IMPORTANT,
                SacredPriority.IMPORTANT: SacredPriority.SACRED
            }
            base_priority = priority_elevation.get(base_priority, base_priority)
        
        return base_priority
    
    def _get_storage_path(self, document_type: DocumentType, document_id: str, 
                         filename: str) -> str:
        """Generate storage path based on document type"""
        type_directories = {
            DocumentType.CEREMONIAL_SCROLL: "ceremonial_scrolls",
            DocumentType.SACRED_CONTRACT: "sacred_contracts", 
            DocumentType.FLAME_BLESSING: "flame_blessings",
            DocumentType.LITURGICAL_TEXT: "liturgical_texts",
            DocumentType.TREASURY_RECORD: "treasury_records",
            DocumentType.COUNCIL_DECREE: "council_decrees",
            DocumentType.WISDOM_CODEX: "wisdom_codices",
            DocumentType.HONOR_CITATION: "honor_citations",
            DocumentType.BINDING_OATH: "binding_oaths",
            DocumentType.ARCHIVE_DOCUMENT: "archive_documents"
        }
        
        directory = type_directories.get(document_type, "archive_documents")
        
        # Use document ID as filename to ensure uniqueness
        file_extension = Path(filename).suffix
        safe_filename = f"{document_id}{file_extension}"
        
        return f"documents/{directory}/{safe_filename}"
    
    async def _save_to_postgres(self, document: SacredDocument) -> bool:
        """Save document metadata to PostgreSQL"""
        if not self.postgres_url or not asyncpg:
            print("⚠️  PostgreSQL URL not configured or asyncpg not available - skipping database storage")
            return False
        
        try:
            conn = await asyncpg.connect(self.postgres_url)
            
            # Create table if not exists
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS sacred_documents (
                    document_id VARCHAR PRIMARY KEY,
                    filename VARCHAR NOT NULL,
                    original_name VARCHAR NOT NULL,
                    file_size BIGINT NOT NULL,
                    content_hash VARCHAR NOT NULL,
                    mime_type VARCHAR,
                    document_type VARCHAR NOT NULL,
                    priority VARCHAR NOT NULL,
                    status VARCHAR NOT NULL,
                    upload_timestamp TIMESTAMPTZ NOT NULL,
                    sacred_binding VARCHAR NOT NULL,
                    ceremonial_seal VARCHAR NOT NULL,
                    uploader_id VARCHAR,
                    storage_path VARCHAR NOT NULL,
                    metadata JSONB,
                    treasury_cost DECIMAL(10,6),
                    flame_blessing TEXT,
                    archive_location VARCHAR,
                    validation_errors JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
            
            # Insert document
            await conn.execute('''
                INSERT INTO sacred_documents (
                    document_id, filename, original_name, file_size, content_hash,
                    mime_type, document_type, priority, status, upload_timestamp,
                    sacred_binding, ceremonial_seal, uploader_id, storage_path,
                    metadata, treasury_cost, flame_blessing, archive_location,
                    validation_errors
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
            ''', 
                document.document_id, document.filename, document.original_name,
                document.file_size, document.content_hash, document.mime_type,
                document.document_type.value, document.priority.value, 
                document.status.value, document.upload_timestamp,
                document.sacred_binding, document.ceremonial_seal,
                document.uploader_id, document.storage_path,
                json.dumps(document.metadata), document.treasury_cost,
                document.flame_blessing, document.archive_location,
                json.dumps(document.validation_errors) if document.validation_errors else None
            )
            
            await conn.close()
            return True
            
        except Exception as e:
            print(f"❌ PostgreSQL storage error: {e}")
            return False
    
    async def _save_metadata_file(self, document: SacredDocument) -> bool:
        """Save document metadata as JSON file"""
        try:
            metadata_path = self.storage_root / "metadata" / f"{document.document_id}.json"
            
            # Convert document to dict with proper enum serialization
            document_dict = asdict(document)
            document_dict['document_type'] = document.document_type.value
            document_dict['priority'] = document.priority.value
            document_dict['status'] = document.status.value
            
            if aiofiles:
                async with aiofiles.open(metadata_path, 'w') as f:
                    await f.write(json.dumps(document_dict, indent=2, default=str))
            else:
                # Fallback to synchronous file operations
                with open(metadata_path, 'w') as f:
                    f.write(json.dumps(document_dict, indent=2, default=str))
            
            return True
            
        except Exception as e:
            print(f"❌ Metadata file save error: {e}")
            return False
    
    async def _save_binding_record(self, document: SacredDocument) -> bool:
        """Save sacred binding record for verification"""
        try:
            binding_path = self.storage_root / "bindings" / f"{document.document_id}.binding"
            
            binding_record = {
                'document_id': document.document_id,
                'sacred_binding': document.sacred_binding,
                'ceremonial_seal': document.ceremonial_seal,
                'content_hash': document.content_hash,
                'timestamp': document.upload_timestamp,
                'verification_signature': f"VERIFIED-BY-ETERNAL-FLAME-{document.ceremonial_seal}"
            }
            
            if aiofiles:
                async with aiofiles.open(binding_path, 'w') as f:
                    await f.write(json.dumps(binding_record, indent=2))
            else:
                # Fallback to synchronous file operations
                with open(binding_path, 'w') as f:
                    f.write(json.dumps(binding_record, indent=2))
            
            return True
            
        except Exception as e:
            print(f"❌ Binding record save error: {e}")
            return False
    
    async def archive_document(self, file: UploadFile, uploader_id: str = None,
                             document_type: DocumentType = None,
                             priority: SacredPriority = None) -> SacredDocument:
        """Archive a document with sacred bindings"""
        try:
            # Read file contents
            contents = await file.read()
            file_size = len(contents)
            
            # Generate content hash
            content_hash = hashlib.sha256(contents).hexdigest()
            
            # Generate unique document ID
            document_id = f"DOC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Determine document characteristics
            detected_type = document_type or self._determine_document_type(file.filename, file.content_type)
            detected_priority = priority or self._determine_priority(detected_type, file_size)
            
            # Calculate costs
            archive_cost = self._calculate_archive_cost(detected_priority, file_size)
            
            # Generate storage path
            storage_path = self._get_storage_path(detected_type, document_id, file.filename)
            full_storage_path = self.storage_root / storage_path
            
            # Create sacred document
            sacred_doc = SacredDocument(
                document_id=document_id,
                filename=full_storage_path.name,
                original_name=file.filename,
                file_size=file_size,
                content_hash=content_hash,
                mime_type=file.content_type or "application/octet-stream",
                document_type=detected_type,
                priority=detected_priority,
                status=DocumentStatus.RECEIVED,
                upload_timestamp=timestamp,
                sacred_binding="",  # Will be generated
                ceremonial_seal="",  # Will be generated
                uploader_id=uploader_id,
                storage_path=storage_path,
                metadata={
                    'upload_ip': 'unknown',
                    'user_agent': 'unknown',
                    'original_timestamp': timestamp
                },
                treasury_cost=archive_cost,
                flame_blessing="",  # Will be generated
                validation_errors=[]
            )
            
            # Generate sacred binding and seal
            sacred_doc.sacred_binding = self._generate_sacred_binding({
                'filename': file.filename,
                'content_hash': content_hash,
                'upload_timestamp': timestamp,
                'file_size': file_size
            })
            
            sacred_doc.ceremonial_seal = self._generate_ceremonial_seal(sacred_doc)
            sacred_doc.flame_blessing = self._generate_flame_blessing(detected_type, detected_priority)
            
            # Save document file
            full_storage_path.parent.mkdir(parents=True, exist_ok=True)
            if aiofiles:
                async with aiofiles.open(full_storage_path, 'wb') as f:
                    await f.write(contents)
            else:
                # Fallback to synchronous file operations
                with open(full_storage_path, 'wb') as f:
                    f.write(contents)
            
            # Save to PostgreSQL (if available)
            postgres_success = await self._save_to_postgres(sacred_doc)
            
            # Save metadata file
            metadata_success = await self._save_metadata_file(sacred_doc)
            
            # Save binding record
            binding_success = await self._save_binding_record(sacred_doc)
            
            # Allocate treasury resources
            if self.treasury and archive_cost > 0:
                try:
                    self.treasury.allocate_resources(
                        resource_type=ResourceType.CEREMONIAL_TOKENS,
                        amount=archive_cost,
                        actor="Document-Archive-System",
                        realm="STORAGE",
                        capsule="Sacred Document Archive",
                        purpose=f"archive_cost_{document_id}"
                    )
                    print(f"💰 Allocated {archive_cost} Sacred Tokens for archival")
                except Exception as e:
                    print(f"⚠️  Treasury allocation warning: {e}")
            
            # Update status
            sacred_doc.status = DocumentStatus.ARCHIVED
            
            # Log successful archival
            print(f"📜 Sacred document archived: {document_id}")
            print(f"   📁 Type: {detected_type.value}")
            print(f"   ⭐ Priority: {detected_priority.value}")
            print(f"   💾 Size: {file_size:,} bytes")
            print(f"   🔐 Binding: {sacred_doc.sacred_binding}")
            print(f"   🏺 Seal: {sacred_doc.ceremonial_seal}")
            
            return sacred_doc
            
        except Exception as e:
            print(f"❌ Document archival error: {e}")
            raise HTTPException(status_code=500, detail=f"Archival failed: {str(e)}")
    
    async def get_document(self, document_id: str) -> Optional[SacredDocument]:
        """Retrieve document by ID"""
        try:
            # Try PostgreSQL first
            if self.postgres_url and asyncpg:
                conn = await asyncpg.connect(self.postgres_url)
                row = await conn.fetchrow(
                    "SELECT * FROM sacred_documents WHERE document_id = $1", 
                    document_id
                )
                await conn.close()
                
                if row:
                    return SacredDocument(
                        document_id=row['document_id'],
                        filename=row['filename'],
                        original_name=row['original_name'],
                        file_size=row['file_size'],
                        content_hash=row['content_hash'],
                        mime_type=row['mime_type'],
                        document_type=DocumentType(row['document_type']),
                        priority=SacredPriority(row['priority']),
                        status=DocumentStatus(row['status']),
                        upload_timestamp=row['upload_timestamp'].isoformat(),
                        sacred_binding=row['sacred_binding'],
                        ceremonial_seal=row['ceremonial_seal'],
                        uploader_id=row['uploader_id'],
                        storage_path=row['storage_path'],
                        metadata=row['metadata'] or {},
                        treasury_cost=float(row['treasury_cost']) if row['treasury_cost'] else 0.0,
                        flame_blessing=row['flame_blessing'],
                        archive_location=row['archive_location'],
                        validation_errors=row['validation_errors'] or []
                    )
            
            # Fall back to metadata file
            metadata_path = self.storage_root / "metadata" / f"{document_id}.json"
            if metadata_path.exists():
                if aiofiles:
                    async with aiofiles.open(metadata_path, 'r') as f:
                        data = json.loads(await f.read())
                else:
                    # Fallback to synchronous file operations
                    with open(metadata_path, 'r') as f:
                        data = json.loads(f.read())
                    
                    return SacredDocument(
                        document_id=data['document_id'],
                        filename=data['filename'],
                        original_name=data['original_name'],
                        file_size=data['file_size'],
                        content_hash=data['content_hash'],
                        mime_type=data['mime_type'],
                        document_type=DocumentType(data['document_type']),
                        priority=SacredPriority(data['priority']),
                        status=DocumentStatus(data['status']),
                        upload_timestamp=data['upload_timestamp'],
                        sacred_binding=data['sacred_binding'],
                        ceremonial_seal=data['ceremonial_seal'],
                        uploader_id=data['uploader_id'],
                        storage_path=data['storage_path'],
                        metadata=data['metadata'],
                        treasury_cost=data['treasury_cost'],
                        flame_blessing=data['flame_blessing'],
                        archive_location=data.get('archive_location'),
                        validation_errors=data.get('validation_errors', [])
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Document retrieval error: {e}")
            return None
    
    async def get_document_statistics(self) -> Dict[str, Any]:
        """Get sacred archive statistics"""
        try:
            stats = {
                'total_documents': 0,
                'total_size_bytes': 0,
                'documents_by_type': {},
                'documents_by_priority': {},
                'documents_by_status': {},
                'total_treasury_cost': 0.0,
                'storage_locations': {},
                'archive_health': 'excellent'
            }
            
            # Try PostgreSQL first
            if self.postgres_url:
                conn = await asyncpg.connect(self.postgres_url)
                rows = await conn.fetch("SELECT * FROM sacred_documents")
                await conn.close()
                
                for row in rows:
                    stats['total_documents'] += 1
                    stats['total_size_bytes'] += row['file_size']
                    stats['total_treasury_cost'] += float(row['treasury_cost']) if row['treasury_cost'] else 0.0
                    
                    # Count by type
                    doc_type = row['document_type']
                    stats['documents_by_type'][doc_type] = stats['documents_by_type'].get(doc_type, 0) + 1
                    
                    # Count by priority  
                    priority = row['priority']
                    stats['documents_by_priority'][priority] = stats['documents_by_priority'].get(priority, 0) + 1
                    
                    # Count by status
                    status = row['status']
                    stats['documents_by_status'][status] = stats['documents_by_status'].get(status, 0) + 1
            
            else:
                # Fall back to metadata files
                metadata_dir = self.storage_root / "metadata"
                if metadata_dir.exists():
                    for metadata_file in metadata_dir.glob("*.json"):
                        try:
                            if aiofiles:
                                async with aiofiles.open(metadata_file, 'r') as f:
                                    data = json.loads(await f.read())
                            else:
                                # Fallback to synchronous file operations
                                with open(metadata_file, 'r') as f:
                                    data = json.loads(f.read())
                                
                                stats['total_documents'] += 1
                                stats['total_size_bytes'] += data['file_size']
                                stats['total_treasury_cost'] += data['treasury_cost']
                                
                                # Count by categories
                                doc_type = data['document_type']
                                priority = data['priority']
                                status = data['status']
                                
                                stats['documents_by_type'][doc_type] = stats['documents_by_type'].get(doc_type, 0) + 1
                                stats['documents_by_priority'][priority] = stats['documents_by_priority'].get(priority, 0) + 1
                                stats['documents_by_status'][status] = stats['documents_by_status'].get(status, 0) + 1
                                
                        except Exception as e:
                            print(f"⚠️  Error reading metadata file {metadata_file}: {e}")
            
            # Calculate storage locations
            for doc_type in DocumentType:
                type_dir = self.storage_root / "documents" / doc_type.value.replace('_', '_')
                if type_dir.exists():
                    count = len(list(type_dir.glob("*")))
                    if count > 0:
                        stats['storage_locations'][doc_type.value] = count
            
            return stats
            
        except Exception as e:
            print(f"❌ Statistics calculation error: {e}")
            return {'error': str(e)}


# FastAPI Application Setup
app = FastAPI(
    title="Sacred Document Archive API",
    description="Ceremonial document archival system for the Dominion",
    version="1.0.0"
)

# Security
security = HTTPBearer(auto_error=False)

# Global archive instance
archive = SacredDocumentArchive()

# Authentication dependency (placeholder)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from auth token (implement based on your auth system)"""
    if credentials:
        # Implement token validation here
        return f"user_{credentials.credentials[:8]}"  # Placeholder
    return "anonymous_user"


@app.post("/upload/docs", response_model=dict)
async def upload_docs(
    file: UploadFile = File(...),
    document_type: str = None,
    priority: str = None,
    current_user: str = Depends(get_current_user)
):
    """
    Upload and archive sacred documents with ceremonial bindings
    
    - **file**: Document file to archive
    - **document_type**: Optional document type override
    - **priority**: Optional priority override
    """
    try:
        # Convert string parameters to enums if provided
        doc_type_enum = None
        priority_enum = None
        
        if document_type:
            try:
                doc_type_enum = DocumentType(document_type.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid document type: {document_type}")
        
        if priority:
            try:
                priority_enum = SacredPriority(priority.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")
        
        # Archive the document
        sacred_doc = await archive.archive_document(
            file=file,
            uploader_id=current_user,
            document_type=doc_type_enum,
            priority=priority_enum
        )
        
        # Return response
        return {
            "document_id": sacred_doc.document_id,
            "filename": sacred_doc.original_name,
            "status": sacred_doc.status.value,
            "document_type": sacred_doc.document_type.value,
            "priority": sacred_doc.priority.value,
            "file_size": sacred_doc.file_size,
            "sacred_binding": sacred_doc.sacred_binding,
            "ceremonial_seal": sacred_doc.ceremonial_seal,
            "treasury_cost": sacred_doc.treasury_cost,
            "flame_blessing": sacred_doc.flame_blessing,
            "archive_timestamp": sacred_doc.upload_timestamp,
            "message": f"📜 Sacred document archived with eternal flame blessing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Archival ceremony failed: {str(e)}")


@app.get("/docs/{document_id}", response_model=dict)
async def get_document_info(
    document_id: str,
    current_user: str = Depends(get_current_user)
):
    """Get information about an archived document"""
    document = await archive.get_document(document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Sacred document not found in archives")
    
    return {
        "document_id": document.document_id,
        "filename": document.original_name,
        "status": document.status.value,
        "document_type": document.document_type.value,
        "priority": document.priority.value,
        "file_size": document.file_size,
        "content_hash": document.content_hash,
        "sacred_binding": document.sacred_binding,
        "ceremonial_seal": document.ceremonial_seal,
        "treasury_cost": document.treasury_cost,
        "flame_blessing": document.flame_blessing,
        "upload_timestamp": document.upload_timestamp,
        "uploader_id": document.uploader_id,
        "metadata": document.metadata
    }


@app.get("/docs/stats", response_model=dict)
async def get_archive_statistics(current_user: str = Depends(get_current_user)):
    """Get sacred archive statistics and health information"""
    stats = await archive.get_document_statistics()
    
    return {
        "sacred_archive_statistics": stats,
        "archive_keeper": current_user,
        "eternal_flame_status": "burning_bright",
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


@app.get("/docs/types", response_model=dict)
async def get_document_types():
    """Get available document types and priorities"""
    return {
        "document_types": [doc_type.value for doc_type in DocumentType],
        "priority_levels": [priority.value for priority in SacredPriority],
        "status_states": [status.value for status in DocumentStatus],
        "sacred_guidance": "Choose document types and priorities that honor the eternal flame"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Sacred archive health check"""
    return {
        "status": "sacred_flame_burning",
        "archive_system": "operational",
        "eternal_blessing": "active",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Factory function for easy archive creation
def create_sacred_archive(storage_root: str = "./sacred_archives", 
                         postgres_url: str = None) -> SacredDocumentArchive:
    """Create a sacred document archive instance"""
    treasury_instance = None
    if CeremonialTreasury:
        try:
            treasury_instance = CeremonialTreasury()
        except Exception as e:
            print(f"⚠️  Treasury initialization warning: {e}")
    
    return SacredDocumentArchive(
        storage_root=storage_root,
        postgres_url=postgres_url,
        treasury=treasury_instance
    )


if __name__ == "__main__":
    import uvicorn
    
    print("🔥" + "="*60 + "🔥")
    print("   SACRED DOCUMENT ARCHIVE SYSTEM")
    print("   Ceremonial Storage for the Dominion")
    print("🔥" + "="*60 + "🔥")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)