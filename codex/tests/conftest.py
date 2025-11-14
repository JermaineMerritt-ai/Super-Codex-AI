"""
Pytest configuration and shared fixtures for Super-Codex-AI tests
Provides common testing utilities, fixtures, and configuration.
"""

import pytest
import tempfile
import shutil
import json
import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from typing import Generator, Dict, Any
import warnings

# Add the parent directory to the Python path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


# Configure asyncio event loop for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_documents(temp_directory: Path) -> Dict[str, Path]:
    """Create sample documents for testing."""
    documents = {
        "markdown": temp_directory / "test.md",
        "json": temp_directory / "config.json",
        "text": temp_directory / "notes.txt",
        "honor_scroll": temp_directory / "honor_scroll.json"
    }
    
    # Create sample content
    documents["markdown"].write_text("""
# Test Document

This is a test markdown document about the Super-Codex-AI system.

## Features

- Honor system with bronze, silver, gold levels
- RAG-based knowledge retrieval
- Ceremonial scroll generation

## Technical Details

The system uses vector embeddings and similarity search.
    """.strip())
    
    documents["json"].write_text(json.dumps({
        "system": "Super-Codex-AI",
        "version": "1.0.0",
        "features": ["RAG", "Scroll Generation", "Honor System"],
        "config": {
            "chunk_size": 1000,
            "similarity_threshold": 0.7
        }
    }, indent=2))
    
    documents["text"].write_text("""
Notes on system architecture:

1. Vector store for document embeddings
2. Template engine for scroll generation
3. Real-time WebSocket connections
4. Audit trail for governance
    """.strip())
    
    documents["honor_scroll"].write_text(json.dumps({
        "scroll_id": "HSA-TEST-001",
        "replay_token": "HSA-2024-TEST-001",
        "actor": "Test Custodian",
        "realm": "TEST-001",
        "metadata": {
            "honors_awarded": ["Excellence in Testing"],
            "significance": "high",
            "ceremony_type": "recognition"
        }
    }, indent=2))
    
    return documents


@pytest.fixture
def mock_config(temp_directory: Path):
    """Create a mock configuration for testing."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        
        from engine.config import CodexConfig
        
        config = CodexConfig(
            corpus_path=temp_directory / "corpus",
            vector_store_path=temp_directory / "vectors.pkl",
            audit_log_path=temp_directory / "audit.json",
            capsule_registry_path=temp_directory / "capsules.json",
            scroll_templates_path=temp_directory / "templates",
            generated_scrolls_path=temp_directory / "generated",
            chunk_size=500,
            chunk_overlap=50,
            similarity_threshold=0.7,
            max_search_results=5,
            embedding_dimension=1536
        )
        
        # Create necessary directories
        config.corpus_path.mkdir(parents=True, exist_ok=True)
        config.scroll_templates_path.mkdir(parents=True, exist_ok=True)
        config.generated_scrolls_path.mkdir(parents=True, exist_ok=True)
        
        return config


@pytest.fixture
def mock_embedding_model():
    """Create a mock embedding model for testing."""
    from engine.rag import MockEmbeddingModel
    return MockEmbeddingModel()


@pytest.fixture
def sample_embeddings():
    """Generate sample embeddings for testing."""
    import random
    random.seed(42)  # For reproducible tests
    
    embeddings = {
        "honor_system": [random.uniform(-1, 1) for _ in range(1536)],
        "technical_docs": [random.uniform(-1, 1) for _ in range(1536)],
        "governance": [random.uniform(-1, 1) for _ in range(1536)],
        "general": [random.uniform(-1, 1) for _ in range(1536)]
    }
    
    return embeddings


@pytest.fixture
def mock_rag_system():
    """Create a mock RAG system for testing."""
    rag = AsyncMock()
    
    # Configure default return values
    rag.initialize = AsyncMock()
    rag.cleanup = AsyncMock()
    rag.ingest = AsyncMock(return_value={
        "chunks_created": 2,
        "vectors_indexed": 2,
        "success": True
    })
    rag.query = AsyncMock(return_value={
        "success": True,
        "sources": [
            {
                "content": "Mock search result content",
                "metadata": {"file_name": "mock.md", "document_type": "test"}
            }
        ],
        "confidence_score": 85,
        "processing_time": 0.5
    })
    
    return rag


@pytest.fixture
def mock_capsule_registry():
    """Create a mock capsule registry for testing."""
    registry = Mock()
    
    # Configure default capsule
    from scrolls.capsule import CapsuleDefinition, CapsuleType, AccessLevel
    from engine.models.prompts import ScrollType
    
    default_capsule = CapsuleDefinition(
        capsule_id="default_test",
        name="Default Test Capsule",
        capsule_type=CapsuleType.SCHOLAR,
        scroll_type=ScrollType.GENERAL,
        access_level=AccessLevel.PUBLIC,
        template_path="test_template.jinja"
    )
    
    registry.get_capsule.return_value = default_capsule
    registry.check_access.return_value = (True, "Access granted")
    registry.list_capsules.return_value = [default_capsule]
    
    return registry


@pytest.fixture
def mock_prompt_manager():
    """Create a mock prompt manager for testing."""
    manager = Mock()
    
    # Configure default responses
    manager.build_full_prompt.return_value = {
        "system": "You are a helpful AI assistant.",
        "user": "User query goes here.",
        "context": "Relevant context information."
    }
    
    manager.track_prompt_performance.return_value = None
    manager.get_performance_report.return_value = {
        "total_templates": 5,
        "by_scroll_type": {"general": 2, "technical": 2, "governance": 1},
        "top_performers": []
    }
    
    return manager


@pytest.fixture
def sample_scroll_template(temp_directory: Path):
    """Create a sample scroll template for testing."""
    template_content = """
# {{ scroll_title }}

**Query**: {{ query }}
**Generated**: {{ timestamp }}
**Capsule**: {{ capsule_name }}

## Response

{{ main_response }}

{% if sources %}
## Sources

{% for source in sources %}
### {{ source.metadata.file_name or "Unknown" }}

{{ source.content[:100] }}...

{% endfor %}
{% endif %}

---

*Generated by Super-Codex-AI*
    """.strip()
    
    template_path = temp_directory / "test_template.jinja"
    template_path.write_text(template_content)
    
    return template_path


@pytest.fixture
def ceremonial_context():
    """Create sample ceremonial context for testing."""
    from scrolls.capsule import CeremonialContext
    
    return CeremonialContext(
        actor="Test Actor",
        realm="TEST-001",
        authority_level="public",
        ceremony_type="testing",
        significance="routine"
    )


@pytest.fixture
def user_context():
    """Create sample user context for testing."""
    return {
        "authority_level": "public",
        "user_id": "test_user_123",
        "session_id": "test_session_456"
    }


# Test data generators
@pytest.fixture
def sample_query_data():
    """Generate sample query data for testing."""
    return {
        "simple_query": "What is the honor system?",
        "technical_query": "How does the RAG engine work?",
        "governance_query": "Explain ceremonial protocols",
        "complex_query": "Compare honor levels and their technical implementation"
    }


@pytest.fixture
def sample_rag_responses():
    """Generate sample RAG response data for testing."""
    return {
        "successful": {
            "success": True,
            "sources": [
                {
                    "content": "The honor system recognizes exceptional contributions.",
                    "metadata": {"file_name": "honor_system.md", "document_type": "governance"}
                }
            ],
            "confidence_score": 85,
            "processing_time": 0.8
        },
        "no_results": {
            "success": True,
            "sources": [],
            "confidence_score": 0,
            "processing_time": 0.2
        },
        "error": {
            "success": False,
            "error": "Processing error occurred",
            "sources": [],
            "confidence_score": 0,
            "processing_time": 0.1
        }
    }


# Utility functions for tests
def create_test_document(content: str, doc_type: str = "general") -> Dict[str, Any]:
    """Create a standardized test document structure."""
    return {
        "content": content,
        "content_type": "text",
        "analysis": {
            "word_count": len(content.split()),
            "line_count": len(content.splitlines()),
            "document_type": doc_type
        },
        "enhanced_metadata": {
            "file_name": f"test_{doc_type}.txt",
            "document_type": doc_type,
            "created_at": "2024-01-01T00:00:00Z"
        }
    }


def create_test_sources(count: int = 3) -> List[Dict[str, Any]]:
    """Create a list of test sources for RAG responses."""
    sources = []
    for i in range(count):
        sources.append({
            "content": f"Test source content number {i + 1}. Contains information about system component {i + 1}.",
            "metadata": {
                "file_name": f"source_{i + 1}.md",
                "document_type": "test",
                "chunk_id": f"chunk_{i + 1}"
            },
            "similarity": 0.9 - (i * 0.1)  # Decreasing similarity
        })
    return sources


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow-running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add integration marker for integration tests
        if "test_integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add performance marker for performance tests
        if "performance" in item.name.lower():
            item.add_marker(pytest.mark.performance)
        
        # Add slow marker for tests that might take longer
        if any(keyword in item.name.lower() for keyword in ["full_system", "workflow", "batch", "concurrent"]):
            item.add_marker(pytest.mark.slow)