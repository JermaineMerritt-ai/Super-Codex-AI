from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, List

# Security scheme
security = HTTPBearer()

# JWT Settings
SECRET_KEY = os.getenv("JWT_SECRET", "codex-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    username: str
    email: Optional[str] = None
    roles: List[str] = []
    is_active: bool = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Mock user database - replace with real database
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@codex.local",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "roles": ["admin", "council", "custodian"],
        "is_active": True,
    },
    "council": {
        "username": "council",
        "email": "council@codex.local", 
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "roles": ["council"],
        "is_active": True,
    },
    "user": {
        "username": "user",
        "email": "user@codex.local",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "roles": ["user"],
        "is_active": True,
    }
}

def get_user(username: str) -> Optional[UserInDB]:
    """Get user from database"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user credentials"""
    user = get_user(username)
    if not user:
        return None
    # In production, verify hashed password
    if password == "secret":  # Simplified for demo
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    
    return User(
        username=user.username,
        email=user.email, 
        roles=user.roles,
        is_active=user.is_active
    )

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_admin(current_user: User = Depends(get_current_active_user)):
    """Require admin role"""
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_council(current_user: User = Depends(get_current_active_user)):
    """Require council role"""
    if not any(role in current_user.roles for role in ["admin", "council"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Council access required"
        )
    return current_user

def is_admin(user: User) -> bool:
    """Check if user has admin role"""
    return "admin" in user.roles

def is_council(user: User) -> bool:
    """Check if user has council role"""
    return any(role in user.roles for role in ["admin", "council"])