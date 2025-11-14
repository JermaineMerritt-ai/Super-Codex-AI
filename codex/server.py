#!/usr/bin/env python3
"""
Super-Codex-AI Server
Main FastAPI application server for the ceremonial AI system

Integrates all components: core services, engines, scrolls, and data management
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import traceback

# FastAPI and web framework imports
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

# Pydantic models for request/response
from pydantic import BaseModel, Field

# Add codex to path
codex_path = Path(__file__).parent / "codex"
sys.path.insert(0, str(codex_path))

# Import codex components
from core.config import CodexConfig
from core.bus import EventBus, EventHandler
from core.audit import AuditLogger
from core.replay import ReplayManager
from core.identity import IdentityManager
from core.utils import CodexUtils

from engines.axiom import AxiomEngine
from engines.rag import RAGEngine
from engines.sigil import SigilEngine
from engines.oracle import OracleEngine
from engines.lantern import LanternEngine
from engines.flame import FlameEngine

from scrolls.capsule import CapsuleRegistry, ScrollGenerator, CeremonialContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('codex_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Global server state
server_state = {
    "config": None,
    "event_bus": None,
    "audit_logger": None,
    "replay_manager": None,
    "identity_manager": None,
    "utils": None,
    "engines": {},
    "capsule_registry": None,
    "scroll_generator": None,
    "startup_time": None,
    "health_status": "initializing"
}

# Pydantic models for API
class QueryRequest(BaseModel):
    query: str = Field(..., description="The question or request to process")
    capsule_id: Optional[str] = Field(None, description="Specific capsule to use for response")
    user_context: Dict[str, Any] = Field(default_factory=dict, description="User context and preferences")
    ceremonial_context: Optional[Dict[str, Any]] = Field(None, description="Ceremonial context for governance queries")

class QueryResponse(BaseModel):
    success: bool
    query: str
    response: Optional[str] = None
    scroll_content: Optional[str] = None
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: Optional[float] = None
    components: Dict[str, str] = Field(default_factory=dict)
    version: str = "1.0.0"

class CapsulesResponse(BaseModel):
    capsules: List[Dict[str, Any]]
    total_count: int

class AnalysisRequest(BaseModel):
    content: str = Field(..., description="Content to analyze")
    analysis_type: str = Field("general", description="Type of analysis to perform")
    context: Dict[str, Any] = Field(default_factory=dict)

class FlameRequest(BaseModel):
    content: str = Field(..., description="Content to transform")
    flame_type: str = Field("purification", description="Type of flame transformation")
    intensity: float = Field(0.7, ge=0.1, le=1.0, description="Transformation intensity")

# Event handlers
class ServerEventHandler(EventHandler):
    """Handles server-level events"""
    
    async def handle_query_processed(self, event_data: Dict[str, Any]):
        """Handle query processing events"""
        query = event_data.get("query", "unknown")
        processing_time = event_data.get("processing_time", 0)
        success = event_data.get("success", False)
        
        logger.info(f"Query processed: '{query[:50]}...' - Success: {success}, Time: {processing_time:.2f}s")
        
        # Log to audit system
        if server_state.get("audit_logger"):
            await server_state["audit_logger"].log_event(
                event_type="query_processed",
                actor="system",
                details={
                    "query_length": len(query),
                    "processing_time": processing_time,
                    "success": success
                }
            )

# Server lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage server startup and shutdown"""
    # Startup
    logger.info("🚀 Initializing Super-Codex-AI Server")
    await startup_server()
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down Super-Codex-AI Server")
    await shutdown_server()

async def startup_server():
    """Initialize all server components"""
    try:
        server_state["startup_time"] = datetime.now(timezone.utc)
        
        # Initialize configuration
        logger.info("📋 Loading configuration...")
        server_state["config"] = CodexConfig()
        
        # Initialize core services
        logger.info("🔧 Initializing core services...")
        server_state["event_bus"] = EventBus()
        server_state["audit_logger"] = AuditLogger(server_state["config"])
        server_state["replay_manager"] = ReplayManager(server_state["config"])
        server_state["identity_manager"] = IdentityManager(server_state["config"])
        server_state["utils"] = CodexUtils(server_state["config"])
        
        # Register event handlers
        event_handler = ServerEventHandler()
        server_state["event_bus"].subscribe("query_processed", event_handler.handle_query_processed)
        
        # Initialize engines
        logger.info("⚙️ Initializing AI engines...")
        server_state["engines"] = {
            "axiom": AxiomEngine(server_state["config"]),
            "rag": RAGEngine(server_state["config"]),
            "sigil": SigilEngine(server_state["config"]),
            "oracle": OracleEngine(server_state["config"]),
            "lantern": LanternEngine(server_state["config"]),
            "flame": FlameEngine(server_state["config"])
        }
        
        # Initialize RAG system
        logger.info("🔍 Initializing RAG engine...")
        await server_state["engines"]["rag"].initialize()
        
        # Initialize scroll system
        logger.info("📜 Initializing scroll system...")
        server_state["capsule_registry"] = CapsuleRegistry(server_state["config"])
        
        # Mock prompt manager for now
        class MockPromptManager:
            def __init__(self, config):
                self.config = config
        
        server_state["scroll_generator"] = ScrollGenerator(
            server_state["config"],
            server_state["capsule_registry"],
            MockPromptManager(server_state["config"])
        )
        
        server_state["health_status"] = "healthy"
        logger.info("✅ Super-Codex-AI Server initialization complete")
        
    except Exception as e:
        logger.error(f"❌ Server initialization failed: {e}")
        logger.error(traceback.format_exc())
        server_state["health_status"] = "failed"
        raise

async def shutdown_server():
    """Clean shutdown of server components"""
    try:
        # Shutdown engines
        for name, engine in server_state.get("engines", {}).items():
            try:
                if hasattr(engine, 'shutdown'):
                    await engine.shutdown()
                logger.info(f"Shutdown {name} engine")
            except Exception as e:
                logger.error(f"Error shutting down {name} engine: {e}")
        
        # Final audit log
        if server_state.get("audit_logger"):
            await server_state["audit_logger"].log_event(
                event_type="server_shutdown",
                actor="system",
                details={"clean_shutdown": True}
            )
        
        logger.info("🔄 Server shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Create FastAPI application
app = FastAPI(
    title="Super-Codex-AI Server",
    description="Ceremonial AI system with honor-based governance",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# API Routes

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with server information"""
    return {
        "service": "Super-Codex-AI Server",
        "status": server_state.get("health_status", "unknown"),
        "version": "1.0.0",
        "description": "Ceremonial AI system for governance and knowledge"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    current_time = datetime.now(timezone.utc)
    startup_time = server_state.get("startup_time")
    
    uptime = None
    if startup_time:
        uptime = (current_time - startup_time).total_seconds()
    
    # Check component health
    components = {}
    for name, engine in server_state.get("engines", {}).items():
        try:
            if hasattr(engine, 'health_check'):
                health = await engine.health_check()
                components[f"{name}_engine"] = health.get("status", "unknown")
            else:
                components[f"{name}_engine"] = "active"
        except Exception as e:
            components[f"{name}_engine"] = f"error: {str(e)}"
    
    # Check core services
    components["config"] = "active" if server_state.get("config") else "inactive"
    components["event_bus"] = "active" if server_state.get("event_bus") else "inactive"
    components["capsule_registry"] = "active" if server_state.get("capsule_registry") else "inactive"
    
    return HealthResponse(
        status=server_state.get("health_status", "unknown"),
        timestamp=current_time.isoformat(),
        uptime_seconds=uptime,
        components=components
    )

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, background_tasks: BackgroundTasks):
    """Process a query through the RAG system and generate a scroll response"""
    start_time = datetime.now(timezone.utc)
    
    try:
        # Get RAG engine
        rag_engine = server_state["engines"]["rag"]
        scroll_generator = server_state["scroll_generator"]
        
        # Process query through RAG
        logger.info(f"Processing query: {request.query[:100]}...")
        rag_result = await rag_engine.process_query(request.query)
        
        if not rag_result.get("success"):
            raise HTTPException(status_code=500, detail=f"RAG processing failed: {rag_result.get('error')}")
        
        sources = rag_result.get("sources", [])
        
        # Determine capsule to use
        capsule_id = request.capsule_id
        if not capsule_id:
            # Use default capsule based on query type
            capsule_id = "guardian_protocols"  # Default
            
            # Simple capsule selection logic
            query_lower = request.query.lower()
            if any(word in query_lower for word in ["governance", "honor", "council", "authority"]):
                capsule_id = "sovereign_crown"
            elif any(word in query_lower for word in ["career", "resume", "job", "professional"]):
                capsule_id = "career_advancement"
            elif any(word in query_lower for word in ["finance", "money", "budget", "investment"]):
                capsule_id = "financial_wisdom"
            elif any(word in query_lower for word in ["learn", "education", "study", "research"]):
                capsule_id = "scholar_archives"
        
        # Prepare ceremonial context
        ceremonial_context = None
        if request.ceremonial_context:
            ceremonial_context = CeremonialContext(**request.ceremonial_context)
        
        # Generate scroll
        scroll_result = await scroll_generator.generate_scroll(
            capsule_id=capsule_id,
            query=request.query,
            sources=sources,
            rag_result=rag_result,
            user_context=request.user_context,
            ceremonial_context=ceremonial_context
        )
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        # Publish event
        if server_state.get("event_bus"):
            background_tasks.add_task(
                server_state["event_bus"].publish,
                "query_processed",
                {
                    "query": request.query,
                    "capsule_id": capsule_id,
                    "processing_time": processing_time,
                    "success": scroll_result.get("success", False)
                }
            )
        
        if not scroll_result.get("success"):
            raise HTTPException(status_code=500, detail=f"Scroll generation failed: {scroll_result.get('error')}")
        
        return QueryResponse(
            success=True,
            query=request.query,
            response=rag_result.get("response"),
            scroll_content=scroll_result.get("scroll_content"),
            sources=sources,
            metadata={
                "capsule_info": scroll_result.get("capsule_info", {}),
                "scroll_metadata": scroll_result.get("scroll_metadata", {}),
                "rag_metadata": rag_result.get("metadata", {}),
                "processing_time": processing_time
            },
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        logger.error(traceback.format_exc())
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        return QueryResponse(
            success=False,
            query=request.query,
            error=str(e),
            processing_time=processing_time
        )

@app.get("/api/capsules", response_model=CapsulesResponse)
async def list_capsules(
    realm_id: Optional[str] = None,
    capsule_type: Optional[str] = None,
    access_level: Optional[str] = None
):
    """List available capsules with optional filtering"""
    try:
        capsule_registry = server_state["capsule_registry"]
        
        # Convert string parameters to enums if provided
        from scrolls.capsule import CapsuleType, AccessLevel
        
        type_filter = None
        if capsule_type:
            try:
                type_filter = CapsuleType(capsule_type.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid capsule type: {capsule_type}")
        
        access_filter = None
        if access_level:
            try:
                access_filter = AccessLevel(access_level.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid access level: {access_level}")
        
        capsules = capsule_registry.list_capsules(
            realm_id=realm_id,
            capsule_type=type_filter,
            access_level=access_filter
        )
        
        capsule_data = []
        for capsule in capsules:
            capsule_data.append({
                "capsule_id": capsule.capsule_id,
                "name": capsule.name,
                "type": capsule.capsule_type.value,
                "access_level": capsule.access_level.value,
                "description": capsule.description,
                "realm_id": capsule.realm_id,
                "active": capsule.active
            })
        
        return CapsulesResponse(
            capsules=capsule_data,
            total_count=len(capsule_data)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing capsules: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve capsules")

@app.post("/api/analyze")
async def analyze_content(request: AnalysisRequest):
    """Analyze content using AI engines"""
    try:
        analysis_type = request.analysis_type.lower()
        
        if analysis_type == "sigil":
            # Pattern recognition analysis
            sigil_engine = server_state["engines"]["sigil"]
            result = await sigil_engine.recognize_patterns(request.content, request.context)
            
        elif analysis_type == "oracle":
            # Wisdom and insight analysis
            oracle_engine = server_state["engines"]["oracle"]
            result = await oracle_engine.provide_wisdom(request.content, request.context)
            
        elif analysis_type == "lantern":
            # Guidance and navigation analysis
            lantern_engine = server_state["engines"]["lantern"]
            result = await lantern_engine.provide_guidance(request.content, request.context)
            
        else:
            # Default to general analysis
            rag_engine = server_state["engines"]["rag"]
            result = await rag_engine.process_query(f"Analyze this content: {request.content}")
        
        return {"success": True, "analysis": result}
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/transform")
async def transform_content(request: FlameRequest):
    """Transform content using Flame engine"""
    try:
        flame_engine = server_state["engines"]["flame"]
        
        # Create transformation ritual
        from engines.flame import FlameType, TransformationStage
        
        try:
            flame_type = FlameType(request.flame_type.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid flame type: {request.flame_type}")
        
        result = await flame_engine.transform_content(
            content=request.content,
            flame_type=flame_type,
            intensity=request.intensity
        )
        
        return {"success": True, "transformation": result}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transformation error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/status")
async def server_status():
    """Detailed server status information"""
    try:
        status = {
            "server": {
                "health": server_state.get("health_status", "unknown"),
                "startup_time": server_state.get("startup_time", "unknown"),
                "uptime": None
            },
            "engines": {},
            "services": {},
            "statistics": {}
        }
        
        # Calculate uptime
        if server_state.get("startup_time"):
            uptime_seconds = (datetime.now(timezone.utc) - server_state["startup_time"]).total_seconds()
            status["server"]["uptime"] = f"{uptime_seconds:.1f} seconds"
        
        # Engine status
        for name, engine in server_state.get("engines", {}).items():
            try:
                if hasattr(engine, 'get_status'):
                    status["engines"][name] = await engine.get_status()
                else:
                    status["engines"][name] = {"status": "active"}
            except Exception as e:
                status["engines"][name] = {"status": "error", "error": str(e)}
        
        # Service status
        services = ["config", "event_bus", "audit_logger", "capsule_registry"]
        for service in services:
            status["services"][service] = "active" if server_state.get(service) else "inactive"
        
        return status
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return {"error": str(e)}

# Static file serving for documentation
if os.path.exists("docs"):
    app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if app.debug else "An unexpected error occurred"
        }
    )

# Development server
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Super-Codex-AI Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--log-level", default="info", help="Log level")
    
    args = parser.parse_args()
    
    if args.debug:
        app.debug = True
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"🚀 Starting Super-Codex-AI Server on {args.host}:{args.port}")
    
    uvicorn.run(
        "server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower()
    )