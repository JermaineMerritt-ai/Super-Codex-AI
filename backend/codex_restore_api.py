from backend.logging_utils import log_capsule_event
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import subprocess
import os
import datetime

# Import and include the webhooks router
# Import and include the webhooks router
from .api import webhooks
# Import and include the upload router
from .api import upload
# Import and include the outreach engagement router
from services.dominion import outreach_engagement
from .capsule_api import router as capsule_router

app = FastAPI()

app.include_router(webhooks.router)
app.include_router(upload.router, prefix="/api")
app.include_router(outreach_engagement.router)
app.include_router(capsule_router)

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
