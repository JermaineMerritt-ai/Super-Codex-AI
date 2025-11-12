# app/deps.py
import os
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv("CLI_API_KEY"):
        raise HTTPException(401, "Invalid API key")