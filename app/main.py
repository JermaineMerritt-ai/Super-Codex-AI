import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from app.routes import artifacts, ceremonies, governance, identity, recall
from app.routers import authentication
from app.security.auth import get_current_user

# Load environment variables
load_dotenv()

app = FastAPI(title="AXIOM-FLAME API", version="1.0.0")

app.include_router(artifacts.router, prefix="/v1/artifacts", tags=["artifacts"])
app.include_router(ceremonies.router, prefix="/v1/ceremonies", tags=["ceremonies"])
app.include_router(governance.router, prefix="/v1/governance", tags=["governance"])
app.include_router(identity.router, prefix="/v1/identity", tags=["identity"])
app.include_router(recall.router, prefix="/v1/recall", tags=["recall"])
app.include_router(authentication.router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.get('user_id', 'unknown')}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
