import os

DB_URL = os.getenv("DATABASE_URL")  # e.g., postgresql+psycopg2://user:pass@db:5432/codex
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_BUCKET = os.getenv("S3_BUCKET", "codex-archives")
COUNCIL_KEY_PATH = os.getenv("COUNCIL_KEY_PATH", "/keys/council_ed25519")
JWT_SECRET = os.getenv("JWT_SECRET")