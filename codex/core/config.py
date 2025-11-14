from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    VECTOR_DIR: str = "./data/vectors"
    VECTOR_NAME: str = "index.faiss"
    CORPUS_DIR: str = "./data/corpus"
    AUDIT_LOG_PATH: str = "./data/audit.log"
    REPLAY_DIR: str = "./data/replay"
    IDENTITIES_DIR: str = "./data/identities"
    SEALS_DIR: str = "./data/seals"
    TOP_K: int = 6
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    def vector_path(self) -> str:
        Path(self.VECTOR_DIR).mkdir(parents=True, exist_ok=True)
        return str(Path(self.VECTOR_DIR) / self.VECTOR_NAME)

settings = Settings()