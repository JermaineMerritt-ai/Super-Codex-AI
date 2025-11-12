
#! .venv\Scripts\python.exe

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Codex Capsule"}

@app.get("/health")
def health():
    return {"status": "ok"}
