# RAG Engine - Retrieval-Augmented Generation system
import os
import json
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from pathlib import Path

from ..core.config import CodexConfig
from ..core.utils import CodexUtils

class Document:
    """Document structure for RAG system"""
    
    def __init__(self, id: str, content: str, metadata: Dict[str, Any] = None):
        self.id = id
        self.content = content
        self.metadata = metadata or {}
        self.embedding: Optional[np.ndarray] = None

class RAGEngine:
    """Retrieval-Augmented Generation engine for knowledge processing"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.documents: Dict[str, Document] = {}
        self.index_built = False
        
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the corpus"""
        doc_id = CodexUtils.generate_id()
        document = Document(doc_id, content, metadata)
        self.documents[doc_id] = document
        
        # Save to corpus directory
        self._save_document(document)
        
        return doc_id
    
    def _save_document(self, document: Document) -> None:
        """Save document to corpus directory"""
        CodexUtils.ensure_directory(self.config.corpus_dir)
        
        doc_data = {
            "id": document.id,
            "content": document.content,
            "metadata": document.metadata,
            "created_at": CodexUtils.generate_timestamp()
        }
        
        doc_file = os.path.join(self.config.corpus_dir, f"{document.id}.json")
        CodexUtils.save_json(doc_data, doc_file)
    
    def load_corpus(self) -> None:
        """Load all documents from corpus directory"""
        if not os.path.exists(self.config.corpus_dir):
            return
        
        for filename in os.listdir(self.config.corpus_dir):
            if not filename.endswith('.json'):
                continue
            
            file_path = os.path.join(self.config.corpus_dir, filename)
            doc_data = CodexUtils.load_json(file_path)
            
            if doc_data:
                document = Document(
                    id=doc_data["id"],
                    content=doc_data["content"],
                    metadata=doc_data.get("metadata", {})
                )
                self.documents[document.id] = document
    
    def build_index(self) -> bool:
        """Build vector index for documents"""
        if not self.documents:
            return False
        
        try:
            # Simple text-based similarity for now
            # In production, this would use proper embeddings
            self.index_built = True
            
            # Save index metadata
            index_meta = {
                "documents": len(self.documents),
                "built_at": CodexUtils.generate_timestamp(),
                "method": "text_similarity"
            }
            
            CodexUtils.ensure_directory(self.config.vector_store_dir)
            meta_file = os.path.join(self.config.vector_store_dir, "index_meta.json")
            CodexUtils.save_json(index_meta, meta_file)
            
            return True
            
        except Exception as e:
            print(f"Error building index: {e}")
            return False
    
    def search(self, query: str, limit: int = 5) -> List[Tuple[Document, float]]:
        """Search for relevant documents"""
        if not self.index_built:
            self.build_index()
        
        if not self.documents:
            return []
        
        # Simple text-based search (keyword matching)
        query_words = set(query.lower().split())
        results = []
        
        for doc in self.documents.values():
            doc_words = set(doc.content.lower().split())
            
            # Calculate simple overlap score
            overlap = len(query_words.intersection(doc_words))
            total_words = len(query_words)
            
            if overlap > 0:
                score = overlap / total_words
                results.append((doc, score))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def generate_response(self, query: str, context_limit: int = 3) -> Dict[str, Any]:
        """Generate response using retrieved context"""
        
        # Retrieve relevant documents
        relevant_docs = self.search(query, limit=context_limit)
        
        if not relevant_docs:
            return {
                "response": "No relevant information found in the corpus.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Extract context from relevant documents
        context_parts = []
        sources = []
        
        for doc, score in relevant_docs:
            context_parts.append(doc.content[:500])  # Limit context size
            sources.append({
                "document_id": doc.id,
                "score": score,
                "metadata": doc.metadata
            })
        
        context = "\n\n".join(context_parts)
        
        # Generate response based on context
        response = self._generate_contextual_response(query, context)
        
        # Calculate confidence based on retrieval scores
        avg_score = sum(score for _, score in relevant_docs) / len(relevant_docs)
        confidence = min(avg_score * 1.2, 1.0)  # Boost slightly, cap at 1.0
        
        return {
            "response": response,
            "context": context,
            "sources": sources,
            "confidence": confidence,
            "query": query
        }
    
    def _generate_contextual_response(self, query: str, context: str) -> str:
        """Generate response based on query and context"""
        # Simple template-based response generation
        # In production, this would use a proper language model
        
        query_lower = query.lower()
        
        if "what is" in query_lower or "define" in query_lower:
            response_template = "Based on the available information, {topic} refers to concepts found in the corpus. The context suggests: {summary}"
        elif "how to" in query_lower or "how do" in query_lower:
            response_template = "According to the documentation, here's guidance on {topic}: {summary}"
        elif "why" in query_lower:
            response_template = "The reasoning behind {topic} appears to be: {summary}"
        else:
            response_template = "Regarding {topic}, the available information indicates: {summary}"
        
        # Extract key topic from query
        topic_words = [word for word in query.split() if len(word) > 3]
        topic = " ".join(topic_words[:3]) if topic_words else "this topic"
        
        # Create summary from context
        context_sentences = context.split('.')[:3]  # First 3 sentences
        summary = '. '.join(context_sentences).strip()
        
        if not summary.endswith('.'):
            summary += '.'
        
        return response_template.format(topic=topic, summary=summary)
    
    def add_scroll_content(self, scroll_type: str, content: str, 
                          metadata: Dict[str, Any] = None) -> str:
        """Add scroll content to the corpus"""
        scroll_metadata = metadata or {}
        scroll_metadata.update({
            "type": "scroll",
            "scroll_type": scroll_type,
            "source": "codex_scrolls"
        })
        
        return self.add_document(content, scroll_metadata)
    
    def get_corpus_stats(self) -> Dict[str, Any]:
        """Get statistics about the corpus"""
        total_docs = len(self.documents)
        total_chars = sum(len(doc.content) for doc in self.documents.values())
        
        # Document type breakdown
        type_counts = {}
        for doc in self.documents.values():
            doc_type = doc.metadata.get("type", "unknown")
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_characters": total_chars,
            "average_document_size": total_chars / total_docs if total_docs > 0 else 0,
            "index_built": self.index_built,
            "document_types": type_counts
        }
    
    def update_document(self, doc_id: str, content: str = None, 
                       metadata: Dict[str, Any] = None) -> bool:
        """Update an existing document"""
        if doc_id not in self.documents:
            return False
        
        document = self.documents[doc_id]
        
        if content is not None:
            document.content = content
        
        if metadata is not None:
            document.metadata.update(metadata)
        
        # Re-save document
        self._save_document(document)
        
        # Mark index as needing rebuild
        self.index_built = False
        
        return True
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the corpus"""
        if doc_id not in self.documents:
            return False
        
        # Remove from memory
        del self.documents[doc_id]
        
        # Remove file
        doc_file = os.path.join(self.config.corpus_dir, f"{doc_id}.json")
        if os.path.exists(doc_file):
            os.remove(doc_file)
        
        # Mark index as needing rebuild
        self.index_built = False
        
        return True