"""
Authentication routes for Super-Codex-AI system
Provides login, token refresh, and user management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import hashlib
import secrets
import time
from app.auth import create_token, get_user, require_admin, User

router = APIRouter(prefix="/auth", tags=["authentication"])

# Basic authentication for login
basic_auth = HTTPBasic()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    roles: List[str] = ["user"]

class UserResponse(BaseModel):
    username: str
    email: Optional[str]
    name: Optional[str] 
    roles: List[str]
    created_at: str

# Simple in-memory user store (replace with database in production)
USERS_DB = {
    "admin": {
        "password_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # "admin"
        "email": "admin@super-codex-ai.local",
        "name": "System Administrator", 
        "roles": ["admin", "council"],
        "created_at": "2025-11-11T00:00:00Z"
    },
    "council": {
        "password_hash": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",  # "council"
        "email": "council@super-codex-ai.local",
        "name": "Council Member",
        "roles": ["council"],
        "created_at": "2025-11-11T00:00:00Z"
    },
    "user": {
        "password_hash": "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",  # "user"
        "email": "user@super-codex-ai.local", 
        "name": "Standard User",
        "roles": ["user"],
        "created_at": "2025-11-11T00:00:00Z"
    }
}

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user by username and password"""
    user_data = USERS_DB.get(username)
    if not user_data:
        return None
    
    if not verify_password(password, user_data["password_hash"]):
        return None
    
    return {
        "username": username,
        "email": user_data["email"],
        "name": user_data["name"],
        "roles": user_data["roles"]
    }

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """
    Authenticate user and return JWT token
    """
    user_data = authenticate_user(login_request.username, login_request.password)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create JWT token
    expires_in = 60 * 60  # 1 hour
    access_token = create_token(
        sub=user_data["username"],
        roles=user_data["roles"],
        exp_minutes=60,
        email=user_data["email"],
        name=user_data["name"]
    )
    
    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        user={
            "username": user_data["username"],
            "email": user_data["email"],
            "name": user_data["name"],
            "roles": user_data["roles"]
        }
    )

@router.post("/token", response_model=LoginResponse)
async def login_basic(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    """
    Authenticate using HTTP Basic Auth and return JWT token
    """
    user_data = authenticate_user(credentials.username, credentials.password)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    expires_in = 60 * 60
    access_token = create_token(
        sub=user_data["username"],
        roles=user_data["roles"],
        exp_minutes=60,
        email=user_data["email"],
        name=user_data["name"]
    )
    
    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        user=user_data
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(get_user)):
    """
    Get current user information
    """
    user_data = USERS_DB.get(user.sub, {})
    
    return UserResponse(
        username=user.sub,
        email=user.email,
        name=user.name,
        roles=user.roles,
        created_at=user_data.get("created_at", "unknown")
    )

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_request: CreateUserRequest,
    current_user: User = Depends(require_admin)
):
    """
    Create a new user (admin only)
    """
    if user_request.username in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create user entry
    USERS_DB[user_request.username] = {
        "password_hash": hash_password(user_request.password),
        "email": user_request.email,
        "name": user_request.name,
        "roles": user_request.roles,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return UserResponse(
        username=user_request.username,
        email=user_request.email,
        name=user_request.name,
        roles=user_request.roles,
        created_at=USERS_DB[user_request.username]["created_at"]
    )

@router.get("/users", response_model=List[UserResponse])
async def list_users(current_user: User = Depends(require_admin)):
    """
    List all users (admin only)
    """
    users = []
    for username, user_data in USERS_DB.items():
        users.append(UserResponse(
            username=username,
            email=user_data["email"],
            name=user_data["name"],
            roles=user_data["roles"],
            created_at=user_data["created_at"]
        ))
    
    return users

@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(user: User = Depends(get_user)):
    """
    Refresh JWT token for authenticated user
    """
    user_data = USERS_DB.get(user.sub)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    expires_in = 60 * 60
    access_token = create_token(
        sub=user.sub,
        roles=user.roles,
        exp_minutes=60,
        email=user.email,
        name=user.name
    )
    
    return LoginResponse(
        access_token=access_token,
        expires_in=expires_in,
        user={
            "username": user.sub,
            "email": user.email,
            "name": user.name,
            "roles": user.roles
        }
    )

@router.post("/logout")
async def logout(user: User = Depends(get_user)):
    """
    Logout user (token-based, client should discard token)
    """
    return {"message": "Successfully logged out", "username": user.sub}