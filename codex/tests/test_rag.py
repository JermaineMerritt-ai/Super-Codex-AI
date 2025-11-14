"""
Test suite for the Super-Codex-AI RAG system
Comprehensive tests for RAG functionality, vector operations, and document processing.
"""

import pytest
import pytest_asyncio
import asyncio
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any

# Import the modules to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.rag import (
    MockEmbeddingModel, VectorStore, TextSplitter, 
    CodexRAG, DocumentChunk
)
from engine.config import CodexConfig
from engine.ingest import (
    TextProcessor, JSONProcessor, ArtifactProcessor, 
    CodexIngest
)


class TestMockEmbeddingModel:
    """Test the mock embedding model"""
    
    def test_initialization(self):
        """Test model initialization"""
        model = MockEmbeddingModel()
        assert model.dimension == 1536
        assert model.model_name == "mock-embedding-model"
    
    def test_embed_single_text(self):
        """Test embedding a single text"""
        model = MockEmbeddingModel()
        text = "This is a test document about the honor system."
        
        embedding = model.embed(text)
        
        assert len(embedding) == 1536
        assert all(isinstance(x, float) for x in embedding)
        assert -1.0 <= max(embedding) <= 1.0
        assert -1.0 <= min(embedding) <= 1.0
    
    def test_embed_multiple_texts(self):
        """Test embedding multiple texts"""
        model = MockEmbeddingModel()
        texts = [
            "First test document",
            "Second test document",
            "Third test document"
        ]
        
        embeddings = model.embed(texts)
        
        assert len(embeddings) == 3
        assert all(len(emb) == 1536 for emb in embeddings)
    
    def test_embed_deterministic(self):
        """Test that embedding is deterministic for same input"""
        model = MockEmbeddingModel()
        text = "Consistent test text"
        
        embedding1 = model.embed(text)
        embedding2 = model.embed(text)
        
        assert embedding1 == embedding2
    
    def test_embed_different_texts(self):
        """Test that different texts produce different embeddings"""
        model = MockEmbeddingModel()
        text1 = "First unique text"
        text2 = "Second unique text"
        
        embedding1 = model.embed(text1)
        embedding2 = model.embed(text2)
        
        assert embedding1 != embedding2
    
    def test_embed_empty_text(self):
        """Test embedding empty text"""
        model = MockEmbeddingModel()
        
        embedding = model.embed("")
        
        assert len(embedding) == 1536
        assert all(x == 0.0 for x in embedding)


class TestVectorStore:
    """Test the vector store functionality"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def vector_store(self, temp_dir):
        """Create vector store for testing"""
        return VectorStore(dimension=1536, storage_path=temp_dir / "vectors.pkl")
    
    def test_initialization(self, vector_store):
        """Test vector store initialization"""
        assert vector_store.dimension == 1536
        assert len(vector_store.embeddings) == 0
        assert len(vector_store.documents) == 0
        assert len(vector_store.metadata) == 0
    
    def test_add_single_document(self, vector_store):
        """Test adding a single document"""
        doc_id = "test_doc_1"
        embedding = [0.1] * 1536
        document = "Test document content"
        metadata = {"type": "test", "source": "unit_test"}
        
        vector_store.add(doc_id, embedding, document, metadata)
        
        assert len(vector_store.embeddings) == 1
        assert len(vector_store.documents) == 1
        assert len(vector_store.metadata) == 1
        assert vector_store.documents[0] == document
        assert vector_store.metadata[0] == metadata
    
    def test_add_multiple_documents(self, vector_store):
        """Test adding multiple documents"""
        docs = [
            ("doc1", [0.1] * 1536, "Content 1", {"type": "test1"}),
            ("doc2", [0.2] * 1536, "Content 2", {"type": "test2"}),
            ("doc3", [0.3] * 1536, "Content 3", {"type": "test3"})
        ]
        
        for doc_id, embedding, content, metadata in docs:
            vector_store.add(doc_id, embedding, content, metadata)
        
        assert len(vector_store.embeddings) == 3
        assert len(vector_store.documents) == 3
        assert len(vector_store.metadata) == 3
    
    def test_similarity_search(self, vector_store):
        """Test similarity search functionality"""
        # Add some test documents
        docs = [
            ("doc1", [1.0] + [0.0] * 1535, "Honor system documentation", {"type": "governance"}),
            ("doc2", [0.0, 1.0] + [0.0] * 1534, "Technical specifications", {"type": "technical"}),
            ("doc3", [0.5, 0.5] + [0.0] * 1534, "Mixed content document", {"type": "general"})
        ]
        
        for doc_id, embedding, content, metadata in docs:
            vector_store.add(doc_id, embedding, content, metadata)
        
        # Search for document similar to doc1
        query_embedding = [0.9] + [0.1] * 1535
        results = vector_store.similarity_search(query_embedding, k=2, min_similarity=0.0)
        
        assert len(results) == 2
        assert results[0]["content"] == "Honor system documentation"  # Should be most similar
        assert results[0]["similarity"] > results[1]["similarity"]
    
    def test_similarity_threshold(self, vector_store):
        """Test similarity threshold filtering"""
        # Add documents with very different embeddings
        vector_store.add("doc1", [1.0] + [0.0] * 1535, "Content 1", {})
        vector_store.add("doc2", [0.0, 1.0] + [0.0] * 1534, "Content 2", {})
        
        # Search with high threshold
        query_embedding = [1.0] + [0.0] * 1535
        results = vector_store.similarity_search(query_embedding, k=10, min_similarity=0.95)
        
        assert len(results) == 1  # Only doc1 should meet the threshold
        assert results[0]["content"] == "Content 1"
    
    def test_save_and_load(self, vector_store, temp_dir):
        """Test saving and loading vector store"""
        # Add some data
        vector_store.add("doc1", [0.1] * 1536, "Test content", {"type": "test"})
        
        # Save
        vector_store.save()
        
        # Create new instance and load
        new_store = VectorStore(dimension=1536, storage_path=temp_dir / "vectors.pkl")
        new_store.load()
        
        assert len(new_store.embeddings) == 1
        assert new_store.documents[0] == "Test content"
        assert new_store.metadata[0] == {"type": "test"}
    
    def test_remove_document(self, vector_store):
        """Test removing documents"""
        # Add documents
        vector_store.add("doc1", [0.1] * 1536, "Content 1", {})
        vector_store.add("doc2", [0.2] * 1536, "Content 2", {})
        
        assert len(vector_store.documents) == 2
        
        # Remove first document
        vector_store.remove(0)
        
        assert len(vector_store.documents) == 1
        assert vector_store.documents[0] == "Content 2"


class TestTextSplitter:
    """Test the text splitter functionality"""
    
    def test_initialization(self):
        """Test TextSplitter initialization"""
        splitter = TextSplitter(chunk_size=1000, chunk_overlap=100)
        
        assert splitter.chunk_size == 1000
        assert splitter.chunk_overlap == 100
    
    def test_split_short_text(self):
        """Test splitting text shorter than chunk size"""
        splitter = TextSplitter(chunk_size=1000, chunk_overlap=100)
        text = "This is a short text that fits in one chunk."
        
        chunks = splitter.split_text(text)
        
        assert len(chunks) == 1
        assert chunks[0].content == text
    
    def test_split_long_text(self):
        """Test splitting text longer than chunk size"""
        splitter = TextSplitter(chunk_size=50, chunk_overlap=10)
        text = "This is a longer text that will be split into multiple chunks. " * 5  # ~300+ chars
        
        chunks = splitter.split_text(text)
        
        assert len(chunks) > 1
        assert all(len(chunk.content) <= 60 for chunk in chunks)  # chunk_size + some tolerance
        
        # There should be some overlap between consecutive chunks
        overlap_found = False
        for i in range(len(chunks) - 1):
            chunk1_end = chunks[i].content[-10:]  # Last 10 chars
            chunk2_start = chunks[i + 1].content[:10]  # First 10 chars
            if any(word in chunk2_start for word in chunk1_end.split()):
                overlap_found = True
                break
        
        assert overlap_found
    
    def test_split_with_metadata(self):
        """Test splitting with additional metadata"""
        splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
        text = "Test document content."
        metadata = {"document_type": "test", "source": "unit_test"}
        
        chunks = splitter.split_text(text, metadata)
        
        assert len(chunks) == 1
        assert chunks[0].metadata["document_type"] == "test"
        assert chunks[0].metadata["source"] == "unit_test"
        assert "chunk_index" in chunks[0].metadata
        assert "start_position" in chunks[0].metadata
    
    def test_split_empty_text(self):
        """Test splitting empty text"""
        splitter = TextSplitter(chunk_size=1000, chunk_overlap=100)
        
        chunks = splitter.split_text("")
        
        assert len(chunks) == 0


class TestCodexRAG:
    """Test the main RAG system"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def config(self, temp_dir):
        """Create test configuration"""
        config = Mock(spec=CodexConfig)
        config.vector_store_path = temp_dir / "vectors.pkl"
        config.chunk_size = 1000
        config.chunk_overlap = 200
        config.similarity_threshold = 0.7
        config.max_search_results = 5
        config.embedding_dimension = 1536
        return config
    
    @pytest_asyncio.fixture
    async def rag_system(self, config):
        """Create RAG system for testing"""
        rag = CodexRAG(config)
        await rag.initialize()
        return rag
    
    @pytest.mark.asyncio
    async def test_initialization(self, rag_system):
        """Test RAG system initialization"""
        assert rag_system.embedding_model is not None
        assert rag_system.vector_store is not None
        assert rag_system.text_splitter is not None
    
    @pytest.mark.asyncio
    async def test_ingest_single_document(self, rag_system):
        """Test ingesting a single document"""
        content = "This is a test document about the Super-Codex-AI honor system."
        metadata = {"document_type": "test", "source": "unit_test"}
        
        result = await rag_system.ingest(content, "test", metadata)
        
        assert result["success"] is True
        assert result["chunks_created"] >= 1
        assert result["vectors_indexed"] >= 1
        assert len(rag_system.vector_store.documents) >= 1
    
    @pytest.mark.asyncio
    async def test_ingest_multiple_documents(self, rag_system):
        """Test ingesting multiple documents"""
        documents = [
            ("Honor system documentation", "governance", {"type": "governance"}),
            ("Technical specifications", "technical", {"type": "technical"}),
            ("General information", "general", {"type": "general"})
        ]
        
        total_chunks = 0
        for content, doc_type, metadata in documents:
            result = await rag_system.ingest(content, doc_type, metadata)
            assert result["success"] is True
            total_chunks += result["chunks_created"]
        
        assert len(rag_system.vector_store.documents) == total_chunks
    
    @pytest.mark.asyncio
    async def test_query_with_results(self, rag_system):
        """Test querying with expected results"""
        # First, ingest some documents
        await rag_system.ingest(
            "The honor system is central to Super-Codex-AI governance.",
            "governance",
            {"topic": "honor_system"}
        )
        await rag_system.ingest(
            "Technical documentation for API endpoints.",
            "technical", 
            {"topic": "api"}
        )
        
        # Query for honor system
        result = await rag_system.query(
            "What is the honor system?",
            {"document_type": "governance"}
        )
        
        assert result["success"] is True
        assert len(result["sources"]) > 0
        assert result["confidence_score"] > 0
        assert "honor system" in result["sources"][0]["content"].lower()
    
    @pytest.mark.asyncio
    async def test_query_no_results(self, rag_system):
        """Test querying with no matching results"""
        # Ingest unrelated content
        await rag_system.ingest(
            "Completely unrelated content about cooking.",
            "general",
            {"topic": "cooking"}
        )
        
        # Query for something completely different
        result = await rag_system.query(
            "Advanced quantum physics theories",
            {}
        )
        
        # Should still return success but with low confidence or no sources
        assert result["success"] is True
        assert result["confidence_score"] == 0 or len(result["sources"]) == 0
    
    @pytest.mark.asyncio
    async def test_query_with_context_filter(self, rag_system):
        """Test querying with context filters"""
        # Ingest documents with different types
        await rag_system.ingest(
            "Governance honor protocols",
            "governance",
            {"document_type": "governance", "topic": "honor"}
        )
        await rag_system.ingest(
            "Technical honor implementation",
            "technical",
            {"document_type": "technical", "topic": "honor"}
        )
        
        # Query with filter
        result = await rag_system.query(
            "honor protocols",
            {"document_type": "governance"}
        )
        
        assert result["success"] is True
        if len(result["sources"]) > 0:
            # Should prefer governance documents
            governance_sources = [
                s for s in result["sources"] 
                if s.get("metadata", {}).get("document_type") == "governance"
            ]
            assert len(governance_sources) > 0
    
    @pytest.mark.asyncio
    async def test_cleanup(self, rag_system):
        """Test RAG system cleanup"""
        # Add some data
        await rag_system.ingest("Test content", "test", {})
        
        # Cleanup should not raise errors
        await rag_system.cleanup()
        
        # After cleanup, the system should still be functional
        # (depending on implementation, this might clear data or just close connections)
        assert rag_system.vector_store is not None


class TestDocumentProcessors:
    """Test document processors"""
    
    @pytest.fixture
    def config(self):
        """Mock configuration"""
        return Mock()
    
    def test_text_processor(self, config):
        """Test TextProcessor"""
        processor = TextProcessor(config)
        
        # Test supported types
        assert processor.can_process(Path("test.txt"))
        assert processor.can_process(Path("test.md"))
        assert not processor.can_process(Path("test.pdf"))
    
    @pytest.mark.asyncio
    async def test_text_processor_process(self, config, tmp_path):
        """Test TextProcessor processing"""
        processor = TextProcessor(config)
        
        # Create test file
        test_file = tmp_path / "test.txt"
        test_content = "This is a test document with multiple lines.\nSecond line here."
        test_file.write_text(test_content)
        
        result = await processor.process(test_file)
        
        assert result["content"] == test_content
        assert result["content_type"] == "text"
        assert result["analysis"]["word_count"] > 0
        assert result["analysis"]["line_count"] == 2
    
    def test_json_processor(self, config):
        """Test JSONProcessor"""
        processor = JSONProcessor(config)
        
        assert processor.can_process(Path("test.json"))
        assert not processor.can_process(Path("test.txt"))
    
    @pytest.mark.asyncio
    async def test_json_processor_process(self, config, tmp_path):
        """Test JSONProcessor processing"""
        processor = JSONProcessor(config)
        
        # Create test JSON file
        test_file = tmp_path / "test.json"
        test_data = {
            "title": "Test Document",
            "content": "Test content",
            "metadata": {"type": "test"}
        }
        test_file.write_text(json.dumps(test_data))
        
        result = await processor.process(test_file)
        
        assert result["content_type"] == "json"
        assert result["raw_data"] == test_data
        assert "structure" in result["analysis"]
    
    def test_artifact_processor(self, config):
        """Test ArtifactProcessor"""
        processor = ArtifactProcessor(config)
        
        assert processor.can_process(Path("artifact.json"))
    
    @pytest.mark.asyncio
    async def test_artifact_processor_process(self, config, tmp_path):
        """Test ArtifactProcessor processing"""
        processor = ArtifactProcessor(config)
        
        # Create test artifact file
        test_file = tmp_path / "honor_scroll.json"
        artifact_data = {
            "scroll_id": "HSA-001",
            "replay_token": "HSA-2024-001",
            "actor": "Test Custodian",
            "realm": "PL-001",
            "metadata": {
                "honors_awarded": ["Excellence in Testing"],
                "significance": "high"
            }
        }
        test_file.write_text(json.dumps(artifact_data))
        
        result = await processor.process(test_file)
        
        assert result["content_type"] == "ceremonial_artifact"
        assert result["analysis"]["artifact_type"] == "honor_scroll"
        assert result["analysis"]["honor_level"] == "high"
        assert "Test Custodian" in result["analysis"]["participants"]


class TestCodexIngest:
    """Test the document ingestion system"""
    
    @pytest.fixture
    def config(self, tmp_path):
        """Mock configuration"""
        config = Mock()
        config.corpus_path = tmp_path / "corpus"
        config.batch_size = 5
        return config
    
    @pytest.fixture
    def mock_rag_system(self):
        """Mock RAG system"""
        rag = AsyncMock()
        rag.ingest = AsyncMock(return_value={
            "chunks_created": 2,
            "vectors_indexed": 2,
            "success": True
        })
        return rag
    
    @pytest.fixture
    def ingest_system(self, config, mock_rag_system):
        """Create ingestion system for testing"""
        return CodexIngest(config, mock_rag_system)
    
    @pytest.mark.asyncio
    async def test_ingest_single_file(self, ingest_system, tmp_path):
        """Test ingesting a single file"""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test document content")
        
        result = await ingest_system.ingest_file(test_file)
        
        assert result["document_type"] is not None
        assert "enhanced_metadata" in result
        assert result["enhanced_metadata"]["file_name"] == "test.txt"
    
    @pytest.mark.asyncio
    async def test_ingest_directory(self, ingest_system, tmp_path):
        """Test ingesting a directory"""
        # Create test files
        test_dir = tmp_path / "test_docs"
        test_dir.mkdir()
        
        (test_dir / "doc1.txt").write_text("First document")
        (test_dir / "doc2.md").write_text("Second document")
        (test_dir / "ignore.pdf").write_text("Unsupported file")  # Should be ignored
        
        result = await ingest_system.ingest_directory(test_dir)
        
        assert result["total_files"] == 2  # Only supported files
        assert result["successful"] >= 0
        assert result["failed"] >= 0
        assert result["success_rate"] >= 0
    
    def test_document_type_detection(self, ingest_system):
        """Test automatic document type detection"""
        # Test different file types
        assert ingest_system._detect_document_type(Path("test.md")) == "documentation"
        assert ingest_system._detect_document_type(Path("config.json")) == "configuration"
        assert ingest_system._detect_document_type(Path("app.log")) == "logs"
        assert ingest_system._detect_document_type(Path("honor_scroll.json")) == "ceremonial_artifact"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])