# Orchestration flows and runner routers
from apps.orchestration.flows_api import router as flows_router
from apps.orchestration.runner_api import exec_router

app.include_router(flows_router)
app.include_router(exec_router)
from fastapi import FastAPI
from apps.connector.routes import webhooks, ingest
from apps.connector.utils.logging import init_logging

app = FastAPI(title="Codex Connector Engine")
init_logging(app)

app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

# Orchestration API routers
from apps.orchestration.api import router as wf_router, runs as runs_router
app.include_router(wf_router)
app.include_router(runs_router)

@app.get("/system/health")
def health():
	return {"status": "ok", "service": "connector"}
