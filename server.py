# server.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engines.rag import RAGEngine
from core.audit import log_event
from core.replay import archive
from scrolls.capsule import router as scroll_router
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize Sentry for error tracking
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn and not sentry_dsn.startswith("https://your-sentry-dsn"):
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        integrations=[
            FastApiIntegration(),
            StarletteIntegration(transaction_style="endpoint")
        ],
        send_default_pii=False,  # Don't send personally identifiable information
    )
    print("✅ Sentry error monitoring initialized")
else:
    print("ℹ️ Sentry not configured - update SENTRY_DSN in .env file")

app = FastAPI(title="Sovereign Intelligence Constellation", version="1.0.0")

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codexdominion.app"],  # restrict to your domain
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type","x-api-key"],
)

rag = RAGEngine()

class IngestBody(BaseModel):
    corpus_dir: str | None = None

@app.post("/ingest")
def ingest(body: IngestBody):
    path = rag.ingest(corpus_dir=body.corpus_dir)
    log_event("ingest", {"path": path})
    return {"index_path": path}

@app.get("/health")
def health():
    return {"status": "crowned-immutable-dispatch-ready"}

app.include_router(scroll_router)