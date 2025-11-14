from fastapi import FastAPI
from app.routes import artifacts

app = FastAPI(title="AXIOM-FLAME API", version="1.0.0")

app.include_router(artifacts.router, prefix="/v1/artifacts", tags=["artifacts"])

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8080, reload=True)