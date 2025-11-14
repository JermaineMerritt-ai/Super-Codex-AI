import os
from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables
load_dotenv()

# Load both keys from environment
PRIMARY_KEY = os.getenv("SECRET_KEY")
SECONDARY_KEY = os.getenv("SECRET_KEY_SECONDARY")

security = HTTPBearer()

def decode_token(token: str):
    """
    Attempt to decode JWT with primary key first, then secondary key.
    """
    try:
        return jwt.decode(token, PRIMARY_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        try:
            return jwt.decode(token, SECONDARY_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency for protected routes.
    """
    payload = decode_token(credentials.credentials)
    return payload  # contains claims like role, user_id, etc.