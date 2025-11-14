from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime
from app.models import Identity, IdentityCreate, AuthRequest, Token
import jwt
import hashlib

router = APIRouter()
security = HTTPBearer()

# In-memory storage for demo purposes
identities_db = {}
tokens_db = {}

# Secret key for JWT (in production, use environment variable)
JWT_SECRET = "axiom-flame-secret-key"

def generate_token(identity: Identity) -> str:
    """Generate JWT token for identity"""
    payload = {
        "identity_id": identity.id,
        "actor": identity.actor,
        "realm": identity.realm,
        "authority_level": identity.authority_level,
        "exp": datetime.now().timestamp() + 3600  # 1 hour expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        identity_id = payload.get("identity_id")
        if identity_id in identities_db:
            return identities_db[identity_id]
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[Identity])
async def list_identities():
    """List all identities"""
    return list(identities_db.values())

@router.get("/{identity_id}", response_model=Identity)
async def get_identity(identity_id: str):
    """Get a specific identity by ID"""
    if identity_id not in identities_db:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identities_db[identity_id]

@router.post("/", response_model=Identity)
async def create_identity(identity: IdentityCreate):
    """Create a new identity"""
    identity_id = f"id_{len(identities_db) + 1}"
    
    new_identity = Identity(
        id=identity_id,
        actor=identity.actor,
        realm=identity.realm,
        authority_level=identity.authority_level,
        capsules=identity.capsules,
        created_at=datetime.now(),
        metadata=identity.metadata
    )
    identities_db[identity_id] = new_identity
    return new_identity

@router.post("/authenticate", response_model=Token)
async def authenticate(auth_request: AuthRequest):
    """Authenticate and get access token"""
    # Find identity by actor and realm
    identity = None
    for id_obj in identities_db.values():
        if id_obj.actor == auth_request.actor and id_obj.realm == auth_request.realm:
            identity = id_obj
            break
    
    if not identity:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not identity.active:
        raise HTTPException(status_code=401, detail="Identity is inactive")
    
    # Check capsule access if specified
    if auth_request.capsule and auth_request.capsule not in identity.capsules:
        raise HTTPException(status_code=403, detail="Access to capsule denied")
    
    # Update last accessed
    identity.last_accessed = datetime.now()
    
    # Generate token
    token = generate_token(identity)
    
    return Token(
        access_token=token,
        identity_id=identity.id
    )

@router.get("/me/profile", response_model=Identity)
async def get_my_profile(current_identity: Identity = Depends(verify_token)):
    """Get current authenticated identity profile"""
    return current_identity

@router.post("/verify")
async def verify_access(auth_request: AuthRequest, current_identity: Identity = Depends(verify_token)):
    """Verify access to specific realm/capsule"""
    # Check realm access
    if current_identity.realm != auth_request.realm and current_identity.authority_level not in ["High", "Maximum"]:
        raise HTTPException(status_code=403, detail="Access to realm denied")
    
    # Check capsule access if specified
    if auth_request.capsule:
        if auth_request.capsule not in current_identity.capsules and current_identity.authority_level not in ["High", "Maximum"]:
            raise HTTPException(status_code=403, detail="Access to capsule denied")
    
    return {
        "access_granted": True,
        "actor": current_identity.actor,
        "realm": auth_request.realm,
        "capsule": auth_request.capsule,
        "authority_level": current_identity.authority_level,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/realms")
async def list_realms():
    """List available realms"""
    realms = set()
    for identity in identities_db.values():
        realms.add(identity.realm)
    
    return {
        "realms": list(realms),
        "default_realms": ["PL-001", "ST-007", "Universal:Core-Nexus"]
    }

@router.get("/capsules")
async def list_capsules():
    """List available capsules"""
    capsules = set()
    for identity in identities_db.values():
        capsules.update(identity.capsules)
    
    return {
        "capsules": list(capsules),
        "common_capsules": ["Sovereign Crown", "Genesis Blueprint", "Test Capsule"]
    }
