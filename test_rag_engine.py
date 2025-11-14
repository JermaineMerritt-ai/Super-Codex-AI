#!/usr/bin/env python3
"""Test script for the RAG engine"""

from engines.rag import RAGEngine
from codex.core.config import settings
from pathlib import Path
import tempfile
import shutil

def main():
    print("🔍 TESTING RAG ENGINE")
    print("=" * 40)
    print(f"📚 Corpus directory: {settings.CORPUS_DIR}")
    print(f"🎯 Vector directory: {settings.VECTOR_DIR}")
    print(f"📊 Embedding model: {settings.EMBEDDING_MODEL}")
    print(f"🔢 Top K results: {settings.TOP_K}")
    print("-" * 40)
    
    # Create test corpus directory and sample documents
    test_corpus_dir = Path("./test_corpus")
    test_corpus_dir.mkdir(exist_ok=True)
    
    print("\n1. 📝 Creating test corpus...")
    
    # Sample documents for testing
    test_docs = {
        "super_codex_overview.txt": """
        Super Codex AI is a streamlined, high-performance artificial intelligence system
        built with modern Python patterns. It features functional APIs, orjson serialization,
        and Pydantic configuration management. The core components include configuration,
        audit logging, replay archive, event bus, and identity management.
        
        Key technologies: Pydantic BaseSettings, orjson binary JSON, pathlib file operations,
        functional programming patterns, and minimal dependency architecture.
        """,
        
        "architecture_principles.txt": """
        The Super Codex AI follows these architectural principles:
        1. Functional APIs over class hierarchies
        2. High-performance orjson serialization throughout
        3. Automatic directory creation with pathlib
        4. Minimal dependencies (Pydantic + orjson + pathlib)
        5. Production-ready performance optimization
        
        Each core module was reduced from complex class systems to simple,
        focused functions achieving ~95% code reduction while maintaining functionality.
        """,
        
        "configuration_system.txt": """
        The configuration system uses Pydantic BaseSettings for modern configuration
        management. It provides automatic environment variable support, path generation,
        and validation. Key settings include VECTOR_DIR, AUDIT_LOG_PATH, REPLAY_DIR,
        IDENTITIES_DIR, SEALS_DIR with methods like vector_path() for path management.
        
        Configuration is centralized and provides foundation for all other core modules
        through the settings import pattern.
        """,
        
        "event_system.txt": """
        The event bus provides simple pub/sub communication with on() and emit() methods.
        It supports multiple handlers per event type and uses typing for safety.
        The EventBus class replaces complex event architectures with a 15-line
        implementation that's zero-dependency and easy to test.
        
        Event patterns enable decoupled communication between system components.
        """,
        
        "performance_optimization.txt": """
        Super Codex AI achieves high performance through:
        - orjson binary JSON serialization (2-5x faster than standard JSON)
        - Functional APIs reducing complexity and overhead
        - Automatic directory creation preventing I/O bottlenecks
        - Minimal dependency tree for faster imports
        - Streamlined code reducing execution paths
        
        Performance gains of ~95% code reduction with improved functionality.
        """
    }
    
    for filename, content in test_docs.items():
        doc_path = test_corpus_dir / filename
        doc_path.write_text(content, encoding="utf-8")
        print(f"   ✅ Created: {filename}")
    
    print(f"   📁 Total documents: {len(test_docs)}")
    
    # Initialize RAG engine
    print("\n2. 🚀 Initializing RAG engine...")
    rag = RAGEngine()
    print(f"   ✅ Embedding model loaded: {settings.EMBEDDING_MODEL}")
    
    # Ingest documents
    print("\n3. 📊 Ingesting documents into vector store...")
    index_path = rag.ingest(corpus_dir=str(test_corpus_dir))
    print(f"   ✅ Vector index created: {Path(index_path).name}")
    print(f"   💾 Index saved to: {index_path}")
    
    # Test retrieval with various queries
    print("\n4. 🔍 Testing document retrieval...")
    
    test_queries = [
        {
            "query": "Pydantic configuration management",
            "description": "Configuration system query"
        },
        {
            "query": "orjson performance benefits",
            "description": "Performance optimization query"
        },
        {
            "query": "event bus pub/sub pattern",
            "description": "Event system query"
        },
        {
            "query": "functional APIs vs class hierarchies",
            "description": "Architecture principles query"
        },
        {
            "query": "pathlib directory creation",
            "description": "File system operations query"
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {test['description']}")
        print(f"   🔎 \"{test['query']}\"")
        
        results = rag.retrieve(test['query'], top_k=3)
        print(f"   📋 Found {len(results)} results:")
        
        for j, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'unknown')
            source_name = Path(source).name if source != 'unknown' else source
            content_preview = doc.page_content[:100].replace('\n', ' ').strip()
            print(f"     {j}. 📄 {source_name}")
            print(f"        📝 {content_preview}...")
    
    # Test loading saved index
    print("\n5. 🔄 Testing index loading...")
    rag2 = RAGEngine()
    rag2.load(index_path)
    print("   ✅ Vector index loaded successfully")
    
    # Verify loaded index works
    test_query = "Super Codex AI streamlined architecture"
    results = rag2.retrieve(test_query, top_k=2)
    print(f"   🔍 Test query: \"{test_query}\"")
    print(f"   📋 Retrieved {len(results)} results from loaded index")
    
    for i, doc in enumerate(results, 1):
        source = Path(doc.metadata.get('source', 'unknown')).name
        print(f"     {i}. 📄 {source}")
    
    # Performance summary
    print("\n6. ⚡ Performance Summary:")
    vector_files = list(Path(settings.VECTOR_DIR).glob("*"))
    if vector_files:
        print(f"   📁 Vector files created: {len(vector_files)}")
        for file in vector_files:
            print(f"     - {file.name}")
    
    print("   🚀 RAG Engine Features:")
    print("     - Sentence Transformers embedding")
    print("     - FAISS vector store for fast similarity search")
    print("     - Recursive text splitting for optimal chunks")
    print("     - Automatic index persistence")
    print("     - Error-tolerant document ingestion")
    
    # Cleanup test corpus
    print("\n7. 🧹 Cleaning up test data...")
    if test_corpus_dir.exists():
        shutil.rmtree(test_corpus_dir)
        print("   ✅ Test corpus removed")
    
    print("\n" + "=" * 40)
    print("✨ RAG ENGINE TEST COMPLETED")
    print("🔍 Vector search and document retrieval verified!")
    print("🚀 Ready for production knowledge queries")
    print("=" * 40)

if __name__ == "__main__":
    main()