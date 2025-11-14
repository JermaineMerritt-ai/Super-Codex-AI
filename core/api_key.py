from fastapi import Request, HTTPException
from core.config import settings

def validate_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if not key or key != settings.CLI_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")