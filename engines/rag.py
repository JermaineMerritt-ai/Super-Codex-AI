from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
import glob, os
from pathlib import Path
from codex.core.config import settings
from typing import List

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()
    
    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()

class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformerEmbeddings(settings.EMBEDDING_MODEL)
        self.vs = None

    def ingest(self, corpus_dir: str | None = None, index_path: str | None = None) -> str:
        corpus_dir = corpus_dir or settings.CORPUS_DIR
        index_path = index_path or settings.vector_path()
        files = glob.glob(os.path.join(corpus_dir, "**/*.*"), recursive=True)
        docs = []
        for f in files:
            try:
                with open(f, "rb") as fh:
                    raw = fh.read()
                text = raw.decode(errors="ignore")
                if text.strip():
                    docs.append(Document(page_content=text, metadata={"source": f}))
            except Exception:
                continue
        if not docs:
            docs = [Document(page_content="Codex seed", metadata={"source": "seed"})]
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        vs = FAISS.from_documents(chunks, self.embedder)
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
        vs.save_local(index_path)
        self.vs = vs
        return index_path

    def load(self, index_path: str | None = None):
        index_path = index_path or settings.vector_path()
        self.vs = FAISS.load_local(index_path, self.embedder, allow_dangerous_deserialization=True)

    def retrieve(self, query: str, top_k: int | None = None):
        k = top_k or settings.TOP_K
        return self.vs.similarity_search(query, k=k)