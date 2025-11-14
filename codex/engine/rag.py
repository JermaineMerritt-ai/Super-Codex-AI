"""
Codex RAG System
Advanced Retrieval-Augmented Generation with vector similarity search,
context enhancement, and real-time processing capabilities.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import logging
import hashlib
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pickle

# Note: In production, you would import actual libraries like:
# import openai
# import chromadb
# import langchain
# from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class DocumentChunk:
    """Represents a chunk of a document with metadata"""
    
    def __init__(self, content: str, metadata: Dict[str, Any], chunk_id: str = None):
        self.content = content
        self.metadata = metadata
        self.chunk_id = chunk_id or self._generate_chunk_id()
        self.embedding = None
        self.created_at = datetime.now(timezone.utc)
    
    def _generate_chunk_id(self) -> str:
        """Generate unique chunk ID based on content hash"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()
        return f"chunk_{content_hash[:12]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary representation"""
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "embedding": self.embedding.tolist() if self.embedding is not None else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentChunk":
        """Create chunk from dictionary representation"""
        chunk = cls(
            content=data["content"],
            metadata=data["metadata"],
            chunk_id=data["chunk_id"]
        )
        chunk.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("embedding"):
            chunk.embedding = np.array(data["embedding"])
        return chunk


class MockEmbeddingModel:
    """Mock embedding model for demonstration purposes"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.model_name = "mock-embedding-model"
    
    def embed(self, text):
        """Generate mock embedding for text (sync version for testing)"""
        if isinstance(text, list):
            return [self._embed_single(t) for t in text]
        return self._embed_single(text)
    
    def _embed_single(self, text: str) -> list:
        """Generate deterministic embedding for single text"""
        if not text.strip():
            return [0.0] * self.dimension
        
        # Generate deterministic "embedding" based on text hash
        hash_value = hashlib.md5(text.encode()).hexdigest()
        seed = int(hash_value[:8], 16)
        np.random.seed(seed)
        
        # Generate normalized random vector
        embedding = np.random.normal(0, 0.3, self.dimension)
        embedding = embedding / np.linalg.norm(embedding) if np.linalg.norm(embedding) > 0 else embedding
        
        return embedding.tolist()
    
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate mock embedding for text (async version)"""
        return np.array(self._embed_single(text))
    
    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for batch of texts"""
        return [await self.embed_text(text) for text in texts]


class VectorStore:
    """Simple vector store with similarity search"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.chunks: Dict[str, DocumentChunk] = {}
        self.embeddings: Dict[str, np.ndarray] = {}
        self.metadata_index: Dict[str, List[str]] = {}  # metadata_key -> [chunk_ids]
    
    def add_chunk(self, chunk: DocumentChunk):
        """Add chunk to vector store"""
        if chunk.embedding is None:
            raise ValueError("Chunk must have embedding before adding to store")
        
        self.chunks[chunk.chunk_id] = chunk
        self.embeddings[chunk.chunk_id] = chunk.embedding
        
        # Update metadata index
        for key, value in chunk.metadata.items():
            index_key = f"{key}:{value}"
            if index_key not in self.metadata_index:
                self.metadata_index[index_key] = []
            self.metadata_index[index_key].append(chunk.chunk_id)
    
    def add_chunks(self, chunks: List[DocumentChunk]):
        """Add multiple chunks to vector store"""
        for chunk in chunks:
            self.add_chunk(chunk)
    
    def similarity_search(self, query_embedding: np.ndarray, k: int = 5, 
                         threshold: float = 0.7, 
                         metadata_filters: Optional[Dict[str, Any]] = None) -> List[Tuple[DocumentChunk, float]]:
        """Perform similarity search with optional metadata filtering"""
        if not self.embeddings:
            return []
        
        # Apply metadata filters if specified
        candidate_chunk_ids = set(self.chunks.keys())
        if metadata_filters:
            for key, value in metadata_filters.items():
                index_key = f"{key}:{value}"
                if index_key in self.metadata_index:
                    candidate_chunk_ids &= set(self.metadata_index[index_key])
                else:
                    return []  # No chunks match the filter
        
        # Calculate similarities
        results = []
        for chunk_id in candidate_chunk_ids:
            embedding = self.embeddings[chunk_id]
            similarity = np.dot(query_embedding, embedding)
            
            if similarity >= threshold:
                chunk = self.chunks[chunk_id]
                results.append((chunk, similarity))
        
        # Sort by similarity and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def get_chunk(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get chunk by ID"""
        return self.chunks.get(chunk_id)
    
    def list_chunks(self, metadata_filters: Optional[Dict[str, Any]] = None) -> List[DocumentChunk]:
        """List all chunks with optional metadata filtering"""
        if not metadata_filters:
            return list(self.chunks.values())
        
        # Apply metadata filters
        candidate_chunk_ids = set(self.chunks.keys())
        for key, value in metadata_filters.items():
            index_key = f"{key}:{value}"
            if index_key in self.metadata_index:
                candidate_chunk_ids &= set(self.metadata_index[index_key])
            else:
                return []
        
        return [self.chunks[chunk_id] for chunk_id in candidate_chunk_ids]
    
    def save(self, path: Path):
        """Save vector store to disk"""
        data = {
            "chunks": {chunk_id: chunk.to_dict() for chunk_id, chunk in self.chunks.items()},
            "metadata_index": self.metadata_index,
            "dimension": self.dimension
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Vector store saved to {path}")
    
    def load(self, path: Path):
        """Load vector store from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.dimension = data["dimension"]
        self.metadata_index = data["metadata_index"]
        
        # Reconstruct chunks and embeddings
        self.chunks = {}
        self.embeddings = {}
        for chunk_id, chunk_data in data["chunks"].items():
            chunk = DocumentChunk.from_dict(chunk_data)
            self.chunks[chunk_id] = chunk
            if chunk.embedding is not None:
                self.embeddings[chunk_id] = chunk.embedding
        
        logger.info(f"Vector store loaded from {path} with {len(self.chunks)} chunks")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        document_types = {}
        total_content_length = 0
        
        for chunk in self.chunks.values():
            doc_type = chunk.metadata.get("document_type", "unknown")
            document_types[doc_type] = document_types.get(doc_type, 0) + 1
            total_content_length += len(chunk.content)
        
        return {
            "total_chunks": len(self.chunks),
            "dimension": self.dimension,
            "document_types": document_types,
            "total_content_length": total_content_length,
            "average_chunk_length": total_content_length / len(self.chunks) if self.chunks else 0
        }


class TextSplitter:
    """Text splitter for creating document chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[DocumentChunk]:
        """Split text into overlapping chunks"""
        if not text.strip():
            return []
        
        metadata = metadata or {}
        chunks = []
        
        # Simple character-based splitting with overlap
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If not the last chunk, try to break at word boundary
            if end < len(text):
                # Look for word boundary within last 100 characters
                boundary_search_start = max(start, end - 100)
                word_boundary = text.rfind(' ', boundary_search_start, end)
                
                if word_boundary > start:
                    end = word_boundary + 1
            
            # Extract chunk content
            chunk_content = text[start:end].strip()
            
            if chunk_content:
                # Create chunk with enhanced metadata
                chunk_metadata = {
                    **metadata,
                    "chunk_index": chunk_index,
                    "start_position": start,
                    "end_position": end,
                    "chunk_length": len(chunk_content)
                }
                
                chunk = DocumentChunk(
                    content=chunk_content,
                    metadata=chunk_metadata
                )
                chunks.append(chunk)
                chunk_index += 1
            
            # Move start position (with overlap)
            start = end - self.chunk_overlap
            
            # Ensure progress
            if start <= 0:
                start = end
        
        logger.debug(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def split_document(self, file_path: Path, metadata: Dict[str, Any] = None) -> List[DocumentChunk]:
        """Split document file into chunks"""
        try:
            # Enhanced metadata with file information
            file_metadata = {
                **(metadata or {}),
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "file_modified": datetime.fromtimestamp(file_path.stat().st_mtime, timezone.utc).isoformat()
            }
            
            # Read file content based on extension
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = json.dumps(data, indent=2)
            else:
                # For other file types, read as text (in production, use proper parsers)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            return self.split_text(content, file_metadata)
            
        except Exception as e:
            logger.error(f"Failed to split document {file_path}: {e}")
            return []


class CodexRAG:
    """Main RAG system for Codex"""
    
    def __init__(self, config):
        self.config = config
        self.embedding_model = MockEmbeddingModel(config.vector_dimension)
        self.vector_store = VectorStore(config.vector_dimension)
        self.text_splitter = TextSplitter(config.chunk_size, config.chunk_overlap)
        self.cache = {} if config.cache_enabled else None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Vector store file path
        self.vector_store_path = config.vectors_path / "codex_vectors.pkl"
    
    async def initialize(self):
        """Initialize the RAG system"""
        try:
            # Load existing vector store if available
            if self.vector_store_path.exists():
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.vector_store.load, self.vector_store_path
                )
                logger.info("Existing vector store loaded")
            else:
                logger.info("Starting with empty vector store")
            
            # Auto-ingest documents from corpus if vector store is empty
            if not self.vector_store.chunks and self.config.corpus_path.exists():
                await self._auto_ingest_corpus()
            
            logger.info("RAG system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {e}")
            raise
    
    async def _auto_ingest_corpus(self):
        """Auto-ingest documents from corpus directory"""
        try:
            document_files = []
            
            # Find all documents in corpus
            for ext in ['*.txt', '*.json', '*.md']:
                document_files.extend(self.config.corpus_path.glob(ext))
            
            if document_files:
                logger.info(f"Auto-ingesting {len(document_files)} documents from corpus")
                
                for doc_file in document_files:
                    await self.ingest(file_path=str(doc_file))
                
                logger.info("Auto-ingestion completed")
            
        except Exception as e:
            logger.warning(f"Auto-ingestion failed: {e}")
    
    async def ingest(self, content: Optional[str] = None, file_path: Optional[str] = None,
                    document_type: str = "general", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ingest document content or file into vector store"""
        try:
            metadata = metadata or {}
            metadata.update({
                "document_type": document_type,
                "ingested_at": datetime.now(timezone.utc).isoformat()
            })
            
            # Get chunks from content or file
            if content:
                chunks = self.text_splitter.split_text(content, metadata)
            elif file_path:
                chunks = self.text_splitter.split_document(Path(file_path), metadata)
            else:
                raise ValueError("Either content or file_path must be provided")
            
            if not chunks:
                logger.warning("No chunks created from input")
                return {"chunks_created": 0, "vectors_indexed": 0}
            
            # Generate embeddings for chunks
            contents = [chunk.content for chunk in chunks]
            embeddings = await self.embedding_model.embed_batch(contents)
            
            # Assign embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding
            
            # Add to vector store
            self.vector_store.add_chunks(chunks)
            
            # Save updated vector store
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self.vector_store.save, self.vector_store_path
            )
            
            logger.info(f"Ingested {len(chunks)} chunks from {file_path or 'content'}")
            
            return {
                "chunks_created": len(chunks),
                "vectors_indexed": len(chunks),
                "document_type": document_type,
                "chunk_ids": [chunk.chunk_id for chunk in chunks]
            }
            
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            raise
    
    async def query(self, query: str, context: Optional[Dict[str, Any]] = None,
                   real_time: bool = False) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            context = context or {}
            query_start = datetime.now(timezone.utc)
            
            # Check cache if enabled
            if self.cache and not real_time:
                cache_key = hashlib.md5(f"{query}{json.dumps(context, sort_keys=True)}".encode()).hexdigest()
                if cache_key in self.cache:
                    cached_result = self.cache[cache_key]
                    logger.info("Returning cached result")
                    return cached_result
            
            # Generate query embedding
            query_embedding = await self.embedding_model.embed_text(query)
            
            # Extract metadata filters from context
            metadata_filters = {}
            if context.get("document_type"):
                metadata_filters["document_type"] = context["document_type"]
            
            # Perform similarity search
            search_results = self.vector_store.similarity_search(
                query_embedding,
                k=self.config.max_chunks_per_query,
                threshold=self.config.similarity_threshold,
                metadata_filters=metadata_filters
            )
            
            # Build context from search results
            search_context = []
            sources = []
            
            for chunk, similarity in search_results:
                search_context.append(chunk.content)
                sources.append({
                    "chunk_id": chunk.chunk_id,
                    "similarity": float(similarity),
                    "metadata": chunk.metadata,
                    "content_preview": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
                })
            
            # Generate answer (mock implementation)
            answer = await self._generate_answer(query, search_context, context)
            
            # Calculate confidence based on similarities
            confidence = np.mean([sim for _, sim in search_results]) if search_results else 0.0
            
            processing_time = (datetime.now(timezone.utc) - query_start).total_seconds()
            
            result = {
                "answer": answer,
                "sources": sources,
                "confidence": float(confidence),
                "query": query,
                "processing_time": processing_time,
                "timestamp": query_start.isoformat(),
                "real_time": real_time,
                "context_used": len(search_context) > 0
            }
            
            # Cache result if caching is enabled
            if self.cache and not real_time:
                self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    async def _generate_answer(self, query: str, context: List[str], 
                              additional_context: Dict[str, Any]) -> str:
        """Generate answer based on query and retrieved context"""
        # Mock answer generation (in production, use actual LLM)
        if not context:
            return f"I don't have enough information in my knowledge base to answer your query: '{query}'. Please consider adding relevant documents to the corpus."
        
        # Simple template-based response for demo
        context_summary = f"Based on {len(context)} relevant document sections"
        
        # Mock intelligent response
        if any("honor" in ctx.lower() for ctx in context):
            answer = f"{context_summary}, I can help with honor-related information. Your query about '{query}' relates to our honor system protocols and ceremonial procedures."
        elif any("artifact" in ctx.lower() for ctx in context):
            answer = f"{context_summary}, I found information about artifact management. Regarding '{query}', this connects to our artifact dispatch and ceremonial preservation systems."
        elif any("scroll" in ctx.lower() for ctx in context):
            answer = f"{context_summary}, I can provide scroll-related guidance. Your question '{query}' pertains to our scroll generation and template management capabilities."
        else:
            answer = f"{context_summary}, I found relevant information in the knowledge base. For your query '{query}', here's what I can tell you based on the available documentation."
        
        # Add context-specific details
        if additional_context.get("scroll_type"):
            answer += f" This information can be formatted as a {additional_context['scroll_type']} scroll for ceremonial purposes."
        
        return answer
    
    async def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about ingested documents"""
        try:
            stats = self.vector_store.get_stats()
            stats.update({
                "vector_store_path": str(self.vector_store_path),
                "cache_size": len(self.cache) if self.cache else 0,
                "cache_enabled": self.config.cache_enabled
            })
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get document stats: {e}")
            return {}
    
    async def search_documents(self, query: str, document_type: Optional[str] = None,
                              limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents by text similarity"""
        try:
            query_embedding = await self.embedding_model.embed_text(query)
            
            metadata_filters = {}
            if document_type:
                metadata_filters["document_type"] = document_type
            
            search_results = self.vector_store.similarity_search(
                query_embedding,
                k=limit,
                threshold=0.5,  # Lower threshold for search
                metadata_filters=metadata_filters
            )
            
            return [
                {
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "similarity": float(similarity),
                    "metadata": chunk.metadata
                }
                for chunk, similarity in search_results
            ]
            
        except Exception as e:
            logger.error(f"Document search failed: {e}")
            return []
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            # Save vector store one final time
            if self.vector_store.chunks:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, self.vector_store.save, self.vector_store_path
                )
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            logger.info("RAG system cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")


# Example usage and testing
if __name__ == "__main__":
    async def test_rag():
        from config import CodexConfig
        
        config = CodexConfig()
        rag = CodexRAG(config)
        
        await rag.initialize()
        
        # Test ingestion
        test_content = """
        The Super-Codex-AI system implements a comprehensive honor scroll mechanism
        for recognizing exceptional performance. The system integrates with artifact
        dispatch capabilities to create ceremonial recognition documents.
        """
        
        await rag.ingest(content=test_content, document_type="system_docs")
        
        # Test query
        result = await rag.query("How does the honor system work?")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {len(result['sources'])}")
        
        # Test stats
        stats = await rag.get_document_stats()
        print(f"Document Stats: {stats}")
        
        await rag.cleanup()
    
    asyncio.run(test_rag())