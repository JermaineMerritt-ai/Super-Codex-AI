"""
Codex Document Ingestion Pipeline
Advanced document processing, parsing, and vector indexing for the Super-Codex-AI system
with support for multiple document types and batch processing.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
import logging
import mimetypes
import hashlib
from concurrent.futures import ThreadPoolExecutor

# Document parsing libraries (mock implementations for demo)
import json
import re

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Base class for document processing"""
    
    def __init__(self, config):
        self.config = config
        self.supported_types = []
    
    def can_process(self, file_path: Path) -> bool:
        """Check if processor can handle this file type"""
        return file_path.suffix.lower() in self.supported_types
    
    async def process(self, file_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process document and return structured content"""
        raise NotImplementedError


class TextProcessor(DocumentProcessor):
    """Process plain text documents"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported_types = ['.txt', '.md', '.log']
    
    async def process(self, file_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic text analysis
            word_count = len(content.split())
            line_count = len(content.splitlines())
            char_count = len(content)
            
            return {
                "content": content,
                "analysis": {
                    "word_count": word_count,
                    "line_count": line_count,
                    "char_count": char_count,
                    "estimated_reading_time": word_count / 200  # words per minute
                },
                "content_type": "text",
                "language": "en"  # Mock language detection
            }
            
        except Exception as e:
            logger.error(f"Failed to process text file {file_path}: {e}")
            raise


class JSONProcessor(DocumentProcessor):
    """Process JSON documents"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported_types = ['.json']
    
    async def process(self, file_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert JSON to searchable text
            content = json.dumps(data, indent=2)
            
            # JSON structure analysis
            structure = self._analyze_json_structure(data)
            
            return {
                "content": content,
                "raw_data": data,
                "analysis": {
                    "structure": structure,
                    "size_bytes": len(content.encode('utf-8')),
                    "keys": list(data.keys()) if isinstance(data, dict) else []
                },
                "content_type": "json",
                "searchable_fields": self._extract_searchable_fields(data)
            }
            
        except Exception as e:
            logger.error(f"Failed to process JSON file {file_path}: {e}")
            raise
    
    def _analyze_json_structure(self, data: Any, level: int = 0) -> Dict[str, Any]:
        """Analyze JSON structure recursively"""
        if level > 5:  # Prevent infinite recursion
            return {"type": "deep_structure", "level": level}
        
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys()),
                "nested": {k: self._analyze_json_structure(v, level + 1) 
                          for k, v in data.items() if isinstance(v, (dict, list))}
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_types": list(set(type(item).__name__ for item in data[:10]))  # Sample first 10
            }
        else:
            return {"type": type(data).__name__}
    
    def _extract_searchable_fields(self, data: Any, prefix: str = "") -> List[str]:
        """Extract searchable text fields from JSON"""
        searchable = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, str):
                    searchable.append(f"{current_path}: {value}")
                elif isinstance(value, (dict, list)):
                    searchable.extend(self._extract_searchable_fields(value, current_path))
                else:
                    searchable.append(f"{current_path}: {str(value)}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{prefix}[{i}]" if prefix else f"[{i}]"
                searchable.extend(self._extract_searchable_fields(item, current_path))
        
        return searchable


class ArtifactProcessor(DocumentProcessor):
    """Process ceremonial artifacts and honor scrolls"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported_types = ['.json']  # Artifacts are JSON-based
    
    async def process(self, file_path: Path, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process artifact file with ceremonial context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                artifact_data = json.load(f)
            
            # Check if this is a ceremonial artifact
            is_artifact = bool(
                artifact_data.get('replay_token') or
                artifact_data.get('scroll_id') or
                artifact_data.get('ceremony_type')
            )
            
            if not is_artifact:
                # Fall back to regular JSON processing
                json_processor = JSONProcessor(self.config)
                return await json_processor.process(file_path, metadata)
            
            # Process as ceremonial artifact
            content = self._extract_artifact_content(artifact_data)
            ceremonial_context = self._extract_ceremonial_context(artifact_data)
            
            return {
                "content": content,
                "artifact_data": artifact_data,
                "analysis": {
                    "artifact_type": self._determine_artifact_type(artifact_data),
                    "ceremonial_context": ceremonial_context,
                    "honor_level": self._assess_honor_level(artifact_data),
                    "participants": self._extract_participants(artifact_data)
                },
                "content_type": "ceremonial_artifact",
                "searchable_content": self._create_searchable_content(artifact_data)
            }
            
        except Exception as e:
            logger.error(f"Failed to process artifact file {file_path}: {e}")
            raise
    
    def _extract_artifact_content(self, artifact_data: Dict[str, Any]) -> str:
        """Extract human-readable content from artifact"""
        content_parts = []
        
        # Title and basic info
        if artifact_data.get('title'):
            content_parts.append(f"Title: {artifact_data['title']}")
        
        # Replay token and ceremony info
        if artifact_data.get('replay_token'):
            content_parts.append(f"Replay Token: {artifact_data['replay_token']}")
        
        # Actor and realm information
        if artifact_data.get('actor'):
            content_parts.append(f"Actor: {artifact_data['actor']}")
        
        if artifact_data.get('realm'):
            content_parts.append(f"Realm: {artifact_data['realm']}")
        
        # Honor scroll specific content
        if 'scroll_content' in artifact_data:
            scroll_content = artifact_data['scroll_content']
            for key, value in scroll_content.items():
                if value:
                    content_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        # Metadata content
        if 'metadata' in artifact_data:
            metadata = artifact_data['metadata']
            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if isinstance(value, str):
                        content_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(content_parts)
    
    def _extract_ceremonial_context(self, artifact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract ceremonial context from artifact"""
        context = {}
        
        # Honor information
        if 'honors_awarded' in artifact_data.get('metadata', {}):
            context['honors'] = artifact_data['metadata']['honors_awarded']
        
        # Performance metrics
        if 'performance_metrics' in artifact_data.get('metadata', {}):
            context['performance'] = artifact_data['metadata']['performance_metrics']
        
        # Ceremony type and significance
        if 'ceremony_type' in artifact_data.get('metadata', {}):
            context['ceremony_type'] = artifact_data['metadata']['ceremony_type']
        
        if 'significance' in artifact_data.get('metadata', {}):
            context['significance'] = artifact_data['metadata']['significance']
        
        return context
    
    def _determine_artifact_type(self, artifact_data: Dict[str, Any]) -> str:
        """Determine the type of ceremonial artifact"""
        if artifact_data.get('scroll_id'):
            return "honor_scroll"
        elif artifact_data.get('replay_token', '').startswith('HSA-'):
            return "honor_scroll_artifact"
        elif 'ceremony_type' in artifact_data.get('metadata', {}):
            return artifact_data['metadata']['ceremony_type']
        elif artifact_data.get('intent'):
            return "ceremonial_dispatch"
        else:
            return "unknown_artifact"
    
    def _assess_honor_level(self, artifact_data: Dict[str, Any]) -> str:
        """Assess the honor level of the artifact"""
        metadata = artifact_data.get('metadata', {})
        
        if 'significance' in metadata:
            return metadata['significance']
        elif 'honors_awarded' in metadata:
            honors = metadata['honors_awarded']
            if isinstance(honors, list) and honors:
                if any('Crown' in honor for honor in honors):
                    return "supreme"
                else:
                    return "high"
        elif artifact_data.get('realm') == 'PL-001':
            return "high"
        else:
            return "standard"
    
    def _extract_participants(self, artifact_data: Dict[str, Any]) -> List[str]:
        """Extract participants from artifact"""
        participants = []
        
        if artifact_data.get('actor'):
            participants.append(artifact_data['actor'])
        
        metadata = artifact_data.get('metadata', {})
        if 'contributor' in metadata:
            participants.append(metadata['contributor'])
        
        if 'participants' in metadata:
            if isinstance(metadata['participants'], list):
                participants.extend(metadata['participants'])
        
        return list(set(participants))  # Remove duplicates
    
    def _create_searchable_content(self, artifact_data: Dict[str, Any]) -> str:
        """Create searchable content combining all relevant fields"""
        searchable_parts = []
        
        # Basic fields
        for field in ['title', 'actor', 'realm', 'capsule', 'intent']:
            if artifact_data.get(field):
                searchable_parts.append(str(artifact_data[field]))
        
        # Metadata content
        metadata = artifact_data.get('metadata', {})
        if isinstance(metadata, dict):
            for key, value in metadata.items():
                if isinstance(value, (str, list)):
                    if isinstance(value, list):
                        searchable_parts.extend([str(v) for v in value])
                    else:
                        searchable_parts.append(str(value))
        
        return " ".join(searchable_parts)


class CodexIngest:
    """Main ingestion pipeline for Codex documents"""
    
    def __init__(self, config, rag_system):
        self.config = config
        self.rag_system = rag_system
        self.processors = {
            'text': TextProcessor(config),
            'json': JSONProcessor(config),
            'artifact': ArtifactProcessor(config)
        }
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def ingest_file(self, file_path: Union[str, Path], 
                         document_type: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ingest single file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Auto-detect document type if not provided
            if not document_type:
                document_type = self._detect_document_type(file_path)
            
            # Select appropriate processor
            processor = self._select_processor(file_path, document_type)
            
            # Process document
            processed = await processor.process(file_path, metadata)
            
            # Enhanced metadata
            enhanced_metadata = {
                **(metadata or {}),
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "file_modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime, timezone.utc
                ).isoformat(),
                "document_type": document_type,
                "content_type": processed.get("content_type", "unknown"),
                "processor_used": processor.__class__.__name__,
                "ingestion_id": self._generate_ingestion_id(file_path)
            }
            
            # Merge analysis data into metadata
            if "analysis" in processed:
                enhanced_metadata.update(processed["analysis"])
            
            # Ingest into RAG system
            rag_result = await self.rag_system.ingest(
                content=processed["content"],
                document_type=document_type,
                metadata=enhanced_metadata
            )
            
            return {
                "file_path": str(file_path),
                "document_type": document_type,
                "content_type": processed.get("content_type"),
                "processor": processor.__class__.__name__,
                "enhanced_metadata": enhanced_metadata,
                **rag_result
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest file {file_path}: {e}")
            raise
    
    async def ingest_directory(self, directory_path: Union[str, Path],
                              recursive: bool = True,
                              file_pattern: str = "*") -> Dict[str, Any]:
        """Ingest all files in directory"""
        try:
            directory_path = Path(directory_path)
            if not directory_path.exists() or not directory_path.is_dir():
                raise ValueError(f"Directory not found: {directory_path}")
            
            # Find files to process
            if recursive:
                files = list(directory_path.rglob(file_pattern))
            else:
                files = list(directory_path.glob(file_pattern))
            
            # Filter to supported file types
            supported_files = [f for f in files if f.is_file() and self._is_supported_file(f)]
            
            logger.info(f"Found {len(supported_files)} supported files in {directory_path}")
            
            # Process files in batches
            batch_size = self.config.batch_size
            results = []
            failed = []
            
            for i in range(0, len(supported_files), batch_size):
                batch = supported_files[i:i + batch_size]
                batch_results = await asyncio.gather(
                    *[self.ingest_file(f) for f in batch],
                    return_exceptions=True
                )
                
                for file_path, result in zip(batch, batch_results):
                    if isinstance(result, Exception):
                        failed.append({"file": str(file_path), "error": str(result)})
                        logger.error(f"Failed to ingest {file_path}: {result}")
                    else:
                        results.append(result)
                
                # Log progress
                processed = len(results) + len(failed)
                logger.info(f"Processed {processed}/{len(supported_files)} files")
            
            return {
                "directory": str(directory_path),
                "total_files": len(supported_files),
                "successful": len(results),
                "failed": len(failed),
                "success_rate": len(results) / len(supported_files) if supported_files else 1.0,
                "results": results,
                "failures": failed,
                "total_chunks": sum(r.get("chunks_created", 0) for r in results)
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest directory {directory_path}: {e}")
            raise
    
    def _detect_document_type(self, file_path: Path) -> str:
        """Auto-detect document type based on file characteristics"""
        # Check if it's an artifact based on file location or naming
        if "artifact" in file_path.name.lower() or "honor" in file_path.name.lower():
            return "ceremonial_artifact"
        
        # Check file extension
        ext = file_path.suffix.lower()
        if ext in ['.txt', '.md']:
            return "documentation"
        elif ext == '.json':
            # Try to determine if it's an artifact by peeking at content
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if any(key in data for key in ['replay_token', 'scroll_id', 'ceremony_type']):
                    return "ceremonial_artifact"
            except:
                pass
            return "configuration"
        elif ext == '.log':
            return "logs"
        else:
            return "general"
    
    def _select_processor(self, file_path: Path, document_type: str) -> DocumentProcessor:
        """Select appropriate processor for file"""
        # Use artifact processor for ceremonial documents
        if document_type in ["ceremonial_artifact", "honor_scroll"]:
            return self.processors['artifact']
        
        # Use extension-based selection
        ext = file_path.suffix.lower()
        if ext == '.json':
            return self.processors['json']
        else:
            return self.processors['text']
    
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if file type is supported"""
        ext = file_path.suffix.lower()
        all_supported_types = set()
        for processor in self.processors.values():
            all_supported_types.update(processor.supported_types)
        return ext in all_supported_types
    
    def _generate_ingestion_id(self, file_path: Path) -> str:
        """Generate unique ingestion ID"""
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"ing_{timestamp}_{file_hash}"


# Example usage
if __name__ == "__main__":
    async def test_ingestion():
        from config import CodexConfig
        from rag import CodexRAG
        
        config = CodexConfig()
        rag = CodexRAG(config)
        await rag.initialize()
        
        ingest = CodexIngest(config, rag)
        
        # Test directory ingestion
        if config.corpus_path.exists():
            result = await ingest.ingest_directory(config.corpus_path)
            print(f"Ingestion result: {result}")
        
        await rag.cleanup()
    
    asyncio.run(test_ingestion())