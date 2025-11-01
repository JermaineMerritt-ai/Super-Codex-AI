from fastapi import FastAPI

app = FastAPI()

@app.get("/metrics/capsule/{capsule_id}")
def get_capsule_metrics(capsule_id: str):
    # Placeholder: replace with DB query or monitoring service call
    return {
        "capsule_id": capsule_id,
        "roi": 0.124,
        "drawdown": 0.032,
        "sharpe_like": 1.8,
        "exposure": {"tech": 0.35, "healthcare": 0.20, "energy": 0.15}
    }
