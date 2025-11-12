# app/main.py
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from app.logging_setup import logger
from app.gateway import router as axiom_router
from app.health import router as health_router
from app.deps import require_api_key
from app.authz import require_roles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)  # Health endpoints don't need API key

# Apply role-based authorization to AXIOM routes
# Requires users to have either "operator" or "admin" roles
app.include_router(
    axiom_router, 
    dependencies=[
        Depends(require_api_key),
        Depends(require_roles("operator", "admin"))
    ]
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})