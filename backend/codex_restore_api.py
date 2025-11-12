from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import subprocess
import os
import datetime

# Import logging utils with fallback
try:
    from backend.logging_utils import log_capsule_event
except ImportError:
    def log_capsule_event(*args, **kwargs):
        pass  # Fallback function

# Import routers with fallbacks
try:
    from backend.api import webhooks
    from backend.api import upload
    from backend.capsule_api import router as capsule_router
except ImportError:
    try:
        from api import webhooks
        from api import upload
        from capsule_api import router as capsule_router
    except ImportError:
        # Create minimal fallback routers
        from fastapi import APIRouter
        webhooks = type('', (), {'router': APIRouter()})()
        upload = type('', (), {'router': APIRouter()})()
        capsule_router = APIRouter()

# Import outreach engagement with fallback
try:
    from services.dominion import outreach_engagement
except ImportError:
    try:
        from backend.services.dominion import outreach_engagement
    except ImportError:
        from fastapi import APIRouter
        outreach_engagement = type('', (), {'router': APIRouter()})()

# Import gateway with fallback
try:
    from backend.gateway import router as gateway_router
except ImportError:
    try:
        from gateway import router as gateway_router
    except ImportError:
        from fastapi import APIRouter
        gateway_router = APIRouter()

app = FastAPI()

app.include_router(webhooks.router)
app.include_router(upload.router, prefix="/api")
app.include_router(outreach_engagement.router)
app.include_router(capsule_router)
app.include_router(gateway_router)

@app.post("/api/restore")
async def restore(request: Request):
    data = await request.json()
    backup_dir = data.get("backup_dir")
    if not backup_dir:
        return {"error": "Missing backup_dir"}
    # Log restore start
    with open("codex-restore.log", "a") as log:
        log.write(f"{datetime.datetime.now()} - Restore started: {backup_dir}\n")
    # Run restore script and stream output
    def run_restore():
        process = subprocess.Popen(
            ["./codex-restore.sh", backup_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ},
            text=True
        )
        for line in process.stdout:
            yield line
        process.wait()
        # Log restore end
        with open("codex-restore.log", "a") as log:
            log.write(f"{datetime.datetime.now()} - Restore finished: {backup_dir} (code {process.returncode})\n")
    return StreamingResponse(run_restore(), media_type="text/plain")
