"""
Codex Engine - Main Application
Core orchestration for the Super-Codex-AI RAG system with scroll generation,
audit trails, and real-time processing capabilities.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ledger_system import write_ledger
from artifact_dispatch_system import dispatch_artifact

from config import CodexConfig
from rag import CodexRAG
from audit import CodexAuditor
from replay import QueryReplayer
from models.prompts import PromptManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('codex_engine.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CodexQueryRequest(BaseModel):
    """Request model for codex queries"""
    query: str = Field(..., description="The query to process")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context")
    scroll_type: Optional[str] = Field(default="general", description="Type of scroll to generate")
    include_audit: bool = Field(default=True, description="Include audit trail")
    real_time: bool = Field(default=False, description="Enable real-time processing")


class CodexQueryResponse(BaseModel):
    """Response model for codex queries"""
    query_id: str
    response: str
    scroll_content: Optional[str] = None
    sources: List[Dict[str, Any]] = []
    audit_trail: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = {}
    timestamp: str
    processing_time: float


class CodexIngestRequest(BaseModel):
    """Request model for document ingestion"""
    content: Optional[str] = None
    file_path: Optional[str] = None
    document_type: str = "general"
    metadata: Dict[str, Any] = {}


class CodexEngine:
    """Main Codex Engine orchestrating all components"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Codex Engine"""
        self.config = CodexConfig(config_path)
        self.rag = CodexRAG(self.config)
        self.auditor = CodexAuditor(self.config)
        self.replay_system = QueryReplayer(self.config) 
        self.prompt_manager = PromptManager(self.config)
        
        # Initialize component status
        self.components = {
            "rag": False,
            "auditor": False,
            "replay": False,
            "prompts": False
        }
        
        logger.info("Codex Engine initialized")
    
    async def startup(self):
        """Startup initialization for all components"""
        try:
            # Initialize RAG system
            await self.rag.initialize()
            self.components["rag"] = True
            logger.info("RAG system initialized")
            
            # Initialize audit system
            await self.auditor.initialize()
            self.components["auditor"] = True
            logger.info("Audit system initialized")
            
            # Initialize replay system
            await self.replay.initialize()
            self.components["replay"] = True
            logger.info("Replay system initialized")
            
            # Initialize prompt manager
            await self.prompt_manager.initialize()
            self.components["prompts"] = True
            logger.info("Prompt manager initialized")
            
            # Create startup audit entry
            startup_audit = {
                "action": "codex_engine_startup",
                "components": self.components,
                "config": {
                    "vector_dimension": self.config.vector_dimension,
                    "chunk_size": self.config.chunk_size,
                    "chunk_overlap": self.config.chunk_overlap
                },
                "startup_time": datetime.now(timezone.utc).isoformat()
            }
            
            write_ledger("codex_audit", startup_audit)
            logger.info("Codex Engine startup complete")
            
        except Exception as e:
            logger.error(f"Startup failed: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown cleanup for all components"""
        try:
            # Create shutdown audit entry
            shutdown_audit = {
                "action": "codex_engine_shutdown",
                "components": self.components,
                "shutdown_time": datetime.now(timezone.utc).isoformat()
            }
            
            write_ledger("codex_audit", shutdown_audit)
            
            # Cleanup components
            if hasattr(self.rag, 'cleanup'):
                await self.rag.cleanup()
            
            logger.info("Codex Engine shutdown complete")
            
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
    
    async def process_query(self, request: CodexQueryRequest) -> CodexQueryResponse:
        """Process a query through the complete codex pipeline"""
        start_time = datetime.now(timezone.utc)
        query_id = f"CQ-{start_time.strftime('%Y%m%d%H%M%S')}-{hash(request.query) % 10000:04d}"
        
        try:
            # Create query audit entry
            if request.include_audit:
                query_audit = {
                    "action": "query_initiated", 
                    "query_id": query_id,
                    "query": request.query[:200] + "..." if len(request.query) > 200 else request.query,
                    "scroll_type": request.scroll_type,
                    "real_time": request.real_time,
                    "context_keys": list(request.context.keys()) if request.context else []
                }
                await self.auditor.log_event(query_audit)
            
            # Process query through RAG
            rag_response = await self.rag.query(
                request.query,
                context=request.context,
                real_time=request.real_time
            )
            
            # Generate scroll content if requested
            scroll_content = None
            if request.scroll_type and request.scroll_type != "general":
                scroll_content = await self._generate_scroll(
                    request.scroll_type,
                    rag_response,
                    request.context
                )
            
            # Calculate processing time
            processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            # Build response
            response = CodexQueryResponse(
                query_id=query_id,
                response=rag_response.get("answer", ""),
                scroll_content=scroll_content,
                sources=rag_response.get("sources", []),
                audit_trail=await self.auditor.get_query_trail(query_id) if request.include_audit else None,
                metadata={
                    "scroll_type": request.scroll_type,
                    "real_time": request.real_time,
                    "source_count": len(rag_response.get("sources", [])),
                    "confidence": rag_response.get("confidence", 0.0)
                },
                timestamp=start_time.isoformat(),
                processing_time=processing_time
            )
            
            # Final audit entry
            if request.include_audit:
                completion_audit = {
                    "action": "query_completed",
                    "query_id": query_id,
                    "processing_time": processing_time,
                    "source_count": len(rag_response.get("sources", [])),
                    "scroll_generated": scroll_content is not None
                }
                await self.auditor.log_event(completion_audit)
            
            return response
            
        except Exception as e:
            # Error audit entry
            if request.include_audit:
                error_audit = {
                    "action": "query_failed",
                    "query_id": query_id,
                    "error": str(e),
                    "processing_time": (datetime.now(timezone.utc) - start_time).total_seconds()
                }
                await self.auditor.log_event(error_audit)
            
            logger.error(f"Query processing failed: {e}")
            raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
    
    async def _generate_scroll(self, scroll_type: str, rag_response: Dict[str, Any], 
                             context: Dict[str, Any]) -> str:
        """Generate scroll content based on type and RAG response"""
        try:
            # Get appropriate prompt template
            template = await self.prompt_manager.get_scroll_template(scroll_type)
            
            # Prepare template context
            template_context = {
                "answer": rag_response.get("answer", ""),
                "sources": rag_response.get("sources", []),
                "query_context": context,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "scroll_type": scroll_type
            }
            
            # Render scroll content
            scroll_content = template.render(**template_context)
            
            return scroll_content
            
        except Exception as e:
            logger.warning(f"Scroll generation failed: {e}")
            return None
    
    async def ingest_document(self, request: CodexIngestRequest) -> Dict[str, Any]:
        """Ingest a new document into the codex"""
        try:
            ingest_id = f"CI-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            
            # Process ingestion through RAG
            result = await self.rag.ingest(
                content=request.content,
                file_path=request.file_path,
                document_type=request.document_type,
                metadata=request.metadata
            )
            
            # Audit the ingestion
            ingest_audit = {
                "action": "document_ingested",
                "ingest_id": ingest_id,
                "document_type": request.document_type,
                "metadata": request.metadata,
                "chunks_created": result.get("chunks_created", 0),
                "vectors_indexed": result.get("vectors_indexed", 0)
            }
            await self.auditor.log_event(ingest_audit)
            
            return {
                "ingest_id": ingest_id,
                "status": "success",
                **result
            }
            
        except Exception as e:
            logger.error(f"Document ingestion failed: {e}")
            raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all components"""
        return {
            "status": "healthy" if all(self.components.values()) else "degraded",
            "components": self.components,
            "config": {
                "vector_dimension": self.config.vector_dimension,
                "chunk_size": self.config.chunk_size,
                "data_path": str(self.config.data_path)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Create engine instance
engine = CodexEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    await engine.startup()
    yield
    # Shutdown
    await engine.shutdown()


# Create FastAPI application
app = FastAPI(
    title="Super-Codex-AI Engine",
    description="Advanced RAG system with scroll generation and audit capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return engine.get_health_status()


@app.post("/query", response_model=CodexQueryResponse)
async def process_query(request: CodexQueryRequest):
    """Process a query through the codex system"""
    return await engine.process_query(request)


@app.post("/ingest")
async def ingest_document(request: CodexIngestRequest):
    """Ingest a new document into the codex"""
    return await engine.ingest_document(request)


@app.get("/audit/{query_id}")
async def get_audit_trail(query_id: str):
    """Get audit trail for a specific query"""
    return await engine.auditor.get_query_trail(query_id)


@app.get("/replay/{replay_id}")
async def get_replay(replay_id: str):
    """Get replay information for a specific session"""
    return await engine.replay.get_replay(replay_id)


@app.post("/replay")
async def create_replay(queries: List[str]):
    """Create a replay session from a list of queries"""
    return await engine.replay.create_replay(queries)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)