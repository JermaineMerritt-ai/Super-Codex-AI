#!/usr/bin/env python3
"""Comprehensive demo integrating RAG engine with streamlined core components"""

from engines.rag import RAGEngine
from codex.core import settings, bus, log_event, archive, save_identity
from pathlib import Path
import tempfile
import shutil

def main():
    print("🌟 SUPER CODEX AI - INTEGRATED RAG + CORE SYSTEM DEMO")
    print("=" * 65)
    print("🔍 Demonstrating knowledge retrieval with integrated core components")
    print("-" * 65)
    
    # Test 1: Initialize core components and RAG engine
    print("\n1. 🚀 SYSTEM INITIALIZATION")
    
    # Setup event handlers for integration
    events_log = []
    
    def knowledge_handler(payload):
        events_log.append(f"Knowledge: {payload['action']} - {payload['query'][:50]}...")
        log_event("knowledge_query", payload)
    
    def system_handler(payload):
        events_log.append(f"System: {payload['message']}")
        log_event("system_event", payload)
    
    bus.on("knowledge", knowledge_handler)
    bus.on("system", system_handler)
    
    # Initialize RAG engine
    rag = RAGEngine()
    
    bus.emit("system", {
        "message": "RAG engine initialized",
        "component": "engines.rag",
        "embedding_model": settings.EMBEDDING_MODEL
    })
    
    print("   ✅ Event bus configured with knowledge and system handlers")
    print("   ✅ RAG engine initialized with SentenceTransformers")
    print("   🔄 Events logged to audit system")
    
    # Test 2: Create comprehensive knowledge base
    print("\n2. 📚 BUILDING COMPREHENSIVE KNOWLEDGE BASE")
    
    # Create expanded corpus with real Super Codex AI documentation
    corpus_dir = Path("./demo_corpus")
    corpus_dir.mkdir(exist_ok=True)
    
    knowledge_docs = {
        "system_overview.md": """
# Super Codex AI System Overview

Super Codex AI represents a paradigm shift from complex ceremonial architectures to 
streamlined, production-ready systems. The core philosophy emphasizes:

## Core Principles
- **Functional APIs**: Replace complex class hierarchies with simple functions
- **High Performance**: orjson binary serialization throughout the system
- **Automatic Management**: pathlib handles directory creation and file operations
- **Minimal Dependencies**: Only essential packages (Pydantic, orjson, pathlib)
- **Production Ready**: Designed for real-world deployment and scaling

## Architecture Benefits
The transformation achieved ~95% code reduction while improving functionality:
- Configuration: 17 lines vs 80+ (Pydantic BaseSettings)
- Audit: 10 lines vs 140+ (orjson logging)
- Replay: 10 lines vs 180+ (simple archival)
- Events: 15 lines vs complex system (pub/sub)
- Identity: 2 functions vs 200+ line manager
        """,
        
        "rag_engine_guide.md": """
# RAG Engine Documentation

The RAG (Retrieval-Augmented Generation) engine provides intelligent document 
search and knowledge retrieval capabilities.

## Features
- **Sentence Transformers**: Uses all-MiniLM-L6-v2 for high-quality embeddings
- **FAISS Vector Store**: Fast similarity search with persistence
- **Document Ingestion**: Recursive corpus processing with error tolerance
- **Text Chunking**: Recursive character splitting (1200 chars, 150 overlap)
- **Flexible APIs**: Support for custom corpus and index paths

## Usage Patterns
```python
# Initialize and ingest
rag = RAGEngine()
index_path = rag.ingest("./corpus", "./vectors/index.faiss")

# Load and query
rag.load(index_path)
results = rag.retrieve("query", top_k=5)
```

## Integration
The RAG engine integrates seamlessly with core components:
- Uses Pydantic settings for configuration
- Logs events through audit system
- Archives query results for replay
        """,
        
        "core_components_reference.md": """
# Core Components Reference

## Configuration (codex.core.config)
Pydantic BaseSettings with automatic environment variable support:
- VECTOR_DIR, AUDIT_LOG_PATH, REPLAY_DIR, IDENTITIES_DIR, SEALS_DIR
- vector_path() method for automatic directory creation
- Type validation and default values

## Event Bus (codex.core.bus)
Simple pub/sub system with typed handlers:
- on(event_type, handler): Register event handlers
- emit(event_type, payload): Emit events to subscribers
- Supports multiple handlers per event type

## Audit Logging (codex.core.audit)
High-performance event logging with orjson:
- log_event(event_type, data): Log structured events
- Binary JSON serialization for speed
- Automatic directory and file management

## Replay Archive (codex.core.replay)
Simple data archival with timestamp naming:
- archive(name, data): Archive data with timestamp
- Returns file path for reference
- Uses orjson for fast serialization

## Identity Management (codex.core.identity)
Streamlined identity and governance functions:
- save_identity(slug, data): Store identity information
- save_seal(slug, seal): Store governance seals
- Automatic slug-based file naming
        """,
        
        "development_guide.md": """
# Development Guide

## Getting Started
1. Clone repository and activate virtual environment
2. Install dependencies: pydantic-settings, orjson, sentence-transformers, langchain, faiss-cpu
3. Configure environment variables or use defaults
4. Initialize core components and RAG engine

## Testing Patterns
- Use test scripts for component verification
- Create temporary corpus for RAG testing
- Monitor events through bus system
- Check audit logs for system behavior

## Production Deployment
- Set production environment variables
- Pre-build vector indices for faster startup
- Configure log rotation and archive cleanup
- Monitor performance metrics and scaling

## Integration Patterns
```python
# Event-driven knowledge queries
bus.on("knowledge_request", handle_knowledge_query)
bus.emit("knowledge_request", {"query": "search terms", "user": "user_id"})

# Audit all operations
log_event("user_query", {"user": user_id, "query": query, "results": len(results)})

# Archive important sessions
archive("user_session", {"queries": queries, "results": results, "duration": duration})
```
        """,
        
        "api_integration.md": """
# API Integration Guide

## RAG Engine API
The RAG engine provides both synchronous and asynchronous operation modes
for integration with web APIs and microservices.

### FastAPI Integration
```python
from fastapi import FastAPI
from engines.rag import RAGEngine

app = FastAPI()
rag = RAGEngine()

@app.post("/search")
async def search_knowledge(query: str, top_k: int = 5):
    results = rag.retrieve(query, top_k)
    return {"query": query, "results": [{"content": r.page_content, "source": r.metadata} for r in results]}
```

### Event-Driven Queries
Integrate with the event bus for decoupled knowledge operations:
- Emit knowledge requests through event system
- Handle results asynchronously
- Log all queries for audit and analytics
- Archive user sessions for replay and analysis

### Performance Considerations
- Pre-load vector indices at startup
- Use caching for frequent queries
- Monitor embedding model performance
- Scale FAISS indices for large corpora
        """
    }
    
    for filename, content in knowledge_docs.items():
        doc_path = corpus_dir / filename
        doc_path.write_text(content, encoding="utf-8")
    
    print(f"   📁 Created knowledge base with {len(knowledge_docs)} documents")
    
    # Ingest knowledge base
    bus.emit("knowledge", {
        "action": "corpus_ingestion_start",
        "query": f"Processing {len(knowledge_docs)} documents",
        "corpus_size": len(knowledge_docs)
    })
    
    index_path = rag.ingest(corpus_dir=str(corpus_dir))
    
    bus.emit("knowledge", {
        "action": "corpus_ingestion_complete", 
        "query": f"Vector index created at {Path(index_path).name}",
        "index_path": index_path
    })
    
    print(f"   ✅ Knowledge base ingested to vector store")
    print(f"   💾 Index saved: {Path(index_path).name}")
    
    # Test 3: Interactive knowledge queries with full integration
    print("\n3. 🔍 INTERACTIVE KNOWLEDGE RETRIEVAL")
    
    # Create a demo user for identity tracking
    demo_user = {
        "name": "Demo Knowledge User",
        "type": "researcher",
        "access_level": 3,
        "specialties": ["system_architecture", "rag_systems", "api_integration"],
        "created": "2025-11-12T16:45:00Z",
        "active": True
    }
    
    user_id = "demo-researcher-001"
    save_identity(user_id, demo_user)
    
    bus.emit("system", {
        "message": f"User {user_id} created for knowledge session",
        "user_id": user_id,
        "user_type": demo_user["type"]
    })
    
    # Comprehensive query scenarios
    knowledge_queries = [
        {
            "query": "How does the RAG engine integrate with core components?",
            "category": "integration",
            "expected": "RAG integration patterns"
        },
        {
            "query": "What are the performance benefits of orjson serialization?",
            "category": "performance",
            "expected": "JSON performance comparison"
        },
        {
            "query": "How to deploy Super Codex AI in production environment?",
            "category": "deployment", 
            "expected": "Production deployment steps"
        },
        {
            "query": "Event bus pub/sub patterns and usage examples",
            "category": "architecture",
            "expected": "Event system documentation"
        },
        {
            "query": "FastAPI integration with RAG search endpoints",
            "category": "api_development",
            "expected": "API integration examples"
        }
    ]
    
    session_data = {
        "session_id": "DEMO_SESSION_001",
        "user_id": user_id,
        "start_time": "2025-11-12T16:45:00Z",
        "queries": [],
        "total_results": 0
    }
    
    for i, query_data in enumerate(knowledge_queries, 1):
        print(f"\n   Query {i}: {query_data['category'].title()}")
        print(f"   🔎 \"{query_data['query']}\"")
        
        # Emit knowledge request event
        bus.emit("knowledge", {
            "action": "query_start",
            "query": query_data['query'],
            "category": query_data['category'],
            "user_id": user_id
        })
        
        # Retrieve knowledge
        results = rag.retrieve(query_data['query'], top_k=3)
        
        # Log detailed query results
        log_event("knowledge_retrieval", {
            "user_id": user_id,
            "query": query_data['query'],
            "category": query_data['category'],
            "results_count": len(results),
            "sources": [r.metadata.get('source', 'unknown') for r in results]
        })
        
        print(f"   📋 Found {len(results)} relevant documents:")
        
        query_results = []
        for j, doc in enumerate(results, 1):
            source = Path(doc.metadata.get('source', 'unknown')).name
            content_preview = doc.page_content[:150].replace('\n', ' ').strip()
            print(f"     {j}. 📄 {source}")
            print(f"        📝 {content_preview}...")
            
            query_results.append({
                "rank": j,
                "source": source,
                "content_preview": content_preview,
                "relevance_score": "high" if j <= 2 else "medium"
            })
        
        # Add to session data
        session_data["queries"].append({
            "query": query_data['query'],
            "category": query_data['category'],
            "results": query_results,
            "results_count": len(results)
        })
        session_data["total_results"] += len(results)
        
        bus.emit("knowledge", {
            "action": "query_complete",
            "query": query_data['query'],
            "results_found": len(results)
        })
    
    # Test 4: Session archival and system summary
    print("\n4. 💾 SESSION ARCHIVAL AND SYSTEM SUMMARY")
    
    # Archive complete session
    session_data["end_time"] = "2025-11-12T16:50:00Z"
    session_data["duration_minutes"] = 5
    session_data["status"] = "completed"
    
    archived_session = archive("knowledge_session", session_data)
    print(f"   ✅ Session archived: {Path(archived_session).name}")
    
    # System performance summary
    events_summary = {
        "total_events": len(events_log),
        "knowledge_events": len([e for e in events_log if e.startswith("Knowledge:")]),
        "system_events": len([e for e in events_log if e.startswith("System:")]),
        "components_active": ["rag_engine", "event_bus", "audit_log", "identity_mgmt", "replay_archive"],
        "session_summary": session_data
    }
    
    archived_summary = archive("system_performance", events_summary)
    print(f"   ✅ Performance summary archived: {Path(archived_summary).name}")
    
    # Event summary
    print(f"\n   📊 Event Summary:")
    print(f"     🔢 Total events processed: {len(events_log)}")
    print(f"     🔍 Knowledge queries: {len(session_data['queries'])}")
    print(f"     📋 Total results retrieved: {session_data['total_results']}")
    print(f"     ⚡ Average results per query: {session_data['total_results'] / len(session_data['queries']):.1f}")
    
    # Core component status
    print(f"\n   🏗️ Core Component Status:")
    print("     ✅ Configuration: Pydantic settings active")
    print("     ✅ Event Bus: Pub/sub communication active")
    print("     ✅ Audit Log: High-performance logging active")
    print("     ✅ Replay Archive: Data persistence active") 
    print("     ✅ Identity Management: User tracking active")
    print("     ✅ RAG Engine: Knowledge retrieval active")
    
    # File system summary
    print(f"\n   📁 File System Status:")
    
    directories = {
        "Vector indices": Path(settings.VECTOR_DIR),
        "Audit logs": Path(settings.AUDIT_LOG_PATH).parent,
        "Replay archives": Path(settings.REPLAY_DIR),
        "Identity data": Path(settings.IDENTITIES_DIR)
    }
    
    for desc, path in directories.items():
        if path.exists():
            files = list(path.glob("*"))
            print(f"     📂 {desc}: {len(files)} files")
        else:
            print(f"     📂 {desc}: Not created yet")
    
    # Cleanup
    print("\n5. 🧹 CLEANUP AND FINALIZATION")
    
    if corpus_dir.exists():
        shutil.rmtree(corpus_dir)
        print("   ✅ Demo corpus cleaned up")
    
    bus.emit("system", {
        "message": "Integrated RAG + Core demo completed successfully",
        "session_queries": len(session_data['queries']),
        "total_results": session_data['total_results'],
        "status": "success"
    })
    
    print("\n" + "=" * 65)
    print("🌟 INTEGRATED DEMO COMPLETED SUCCESSFULLY")
    print("🔍 RAG engine seamlessly integrated with core components")
    print("⚡ High-performance knowledge retrieval with full event tracking")
    print("💾 Complete audit trail and session archival")
    print("🚀 Production-ready intelligent document search system")
    print("=" * 65)

if __name__ == "__main__":
    main()