#!/usr/bin/env python3
"""
Direct test of RAG engine to bypass import issues
"""

import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

def test_rag_direct(corpus_path="./data/corpus"):
    """Test RAG engine directly"""
    try:
        # Import RAG components directly
        from sentence_transformers import SentenceTransformer
        from langchain_community.vectorstores import FAISS
        from langchain_core.documents import Document
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.embeddings import Embeddings
        import glob
        from pathlib import Path
        from typing import List
        
        class SentenceTransformerEmbeddings(Embeddings):
            def __init__(self, model_name: str):
                self.model = SentenceTransformer(model_name)
            
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return self.model.encode(texts, normalize_embeddings=True).tolist()
            
            def embed_query(self, text: str) -> List[float]:
                return self.model.encode([text], normalize_embeddings=True)[0].tolist()

        class SimpleRAGEngine:
            def __init__(self):
                self.embedder = SentenceTransformerEmbeddings("sentence-transformers/all-MiniLM-L6-v2")
                self.vs = None

            def ingest(self, corpus_dir: str) -> str:
                vector_dir = "./data/vectors"
                index_path = f"{vector_dir}/index.faiss"
                
                # Create corpus directory if it doesn't exist
                Path(corpus_dir).mkdir(parents=True, exist_ok=True)
                
                files = glob.glob(os.path.join(corpus_dir, "**/*.*"), recursive=True)
                docs = []
                for f in files:
                    try:
                        with open(f, "rb") as fh:
                            raw = fh.read()
                        text = raw.decode(errors="ignore")
                        if text.strip():
                            docs.append(Document(page_content=text, metadata={"source": f}))
                    except Exception as e:
                        print(f"Skipping file {f}: {e}")
                        continue
                        
                if not docs:
                    print("No documents found, creating seed document")
                    docs = [Document(page_content="Super Codex AI - Sovereign Intelligence Constellation", metadata={"source": "seed"})]
                
                splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
                chunks = splitter.split_documents(docs)
                
                print(f"Processing {len(chunks)} chunks from {len(docs)} documents")
                
                vs = FAISS.from_documents(chunks, self.embedder)
                Path(index_path).parent.mkdir(parents=True, exist_ok=True)
                vs.save_local(index_path)
                self.vs = vs
                
                print(f"✅ RAG corpus ingested successfully")
                print(f"📁 Vector index saved to: {index_path}")
                print(f"📚 Processed {len(docs)} documents into {len(chunks)} chunks")
                return index_path

        # Run the ingestion
        rag = SimpleRAGEngine()
        result = rag.ingest(corpus_path)
        return result
        
    except Exception as e:
        print(f"❌ Error in RAG ingestion: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    corpus_path = sys.argv[1] if len(sys.argv) > 1 else "./data/corpus"
    test_rag_direct(corpus_path)