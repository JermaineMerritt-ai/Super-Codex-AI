import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from core.config import settings

security = HTTPBearer()

def create_jwt(data: dict, expires_delta: int = 3600):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(seconds=expires_delta)})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")