import os

class Settings:
    JWT_SECRET = os.getenv("JWT_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    CLI_API_KEY = os.getenv("CLI_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")

    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/vectors/index.faiss")
    AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./data/audit.log")
    REPLAY_ARCHIVE_PATH = os.getenv("REPLAY_ARCHIVE_PATH", "./data/replay/")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

    LEDGER_PATH = os.getenv("LEDGER_PATH", "./storage/ledger")
    ANNALS_PATH = os.getenv("ANNALS_PATH", "./storage/annals")
    REPLAYS_PATH = os.getenv("REPLAYS_PATH", "./storage/replays")

settings = Settings()