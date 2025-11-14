"""
Pydantic models for the AXIOM-FLAME API system.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime
import uuid

# Artifact Models
class ArtifactCreate(BaseModel):
    """Model for creating new ceremonial artifacts."""
    type: Literal["Constitution","Declaration","Anthem","Oath","Ceremony","Handbook","Guide","Proclamation","Compendium","Charter"]
    title: str
    slug: str
    content_uri: str

class Artifact(BaseModel):
    """Model representing a ceremonial artifact."""
    id: str
    type: str
    title: str
    slug: str
    version: str
    status: Literal["draft","sealed"]
    checksum: str
    storage_uri: str
    created_by: str
    created_at: datetime

# Ceremony Models
class CeremonyCreate(BaseModel):
    """Model for creating new ceremonies."""
    kind: Literal["Induction","Continuum","Millennium","Opening","Closing"]
    script_ref: str
    scheduled_at: datetime
    location: str
    council_id: str

class Ceremony(BaseModel):
    """Model representing a ceremony."""
    id: str
    kind: str
    script_ref: str
    scheduled_at: datetime
    location: str
    council_id: str
    status: Literal["scheduled","active","completed","cancelled"]
    created_at: datetime

class OathRecord(BaseModel):
    """Model for recording ceremony oaths."""
    ceremony_id: str
    heir_id: str
    signature: str
    recited_at: datetime

# Governance Models
class GovernanceRule(BaseModel):
    """Model for governance rules."""
    id: str
    name: str
    description: str
    authority_level: str
    seal_type: str
    active: bool = True
    created_at: datetime
    metadata: Optional[dict] = None

class GovernanceRuleCreate(BaseModel):
    """Model for creating governance rules."""
    name: str
    description: str
    authority_level: str = "Standard"
    seal_type: str = "Sacred"
    metadata: Optional[dict] = None

class Council(BaseModel):
    """Model for councils."""
    id: str
    name: str
    members: List[str]
    authority_level: str
    active: bool = True
    created_at: datetime

class CouncilCreate(BaseModel):
    """Model for creating councils."""
    name: str
    members: List[str]
    authority_level: str = "Standard"

# Identity Models  
class Identity(BaseModel):
    """Model representing an identity in the system."""
    id: str
    actor: str
    realm: str
    authority_level: str
    capsules: List[str]
    active: bool = True
    created_at: datetime
    last_accessed: Optional[datetime] = None
    metadata: Optional[dict] = None

class IdentityCreate(BaseModel):
    """Model for creating new identities."""
    actor: str
    realm: str
    authority_level: str = "Standard"
    capsules: List[str] = []
    metadata: Optional[dict] = None

class AuthRequest(BaseModel):
    """Model for authentication requests."""
    actor: str
    realm: str
    capsule: Optional[str] = None

class Token(BaseModel):
    """Model for authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    identity_id: str

# Recall/Memory Models
class RecallEntry(BaseModel):
    """Model for recall entries."""
    id: str
    dispatch_id: str
    timestamp: datetime
    actor: str
    realm: str
    capsule: str
    intent: str
    content: Dict[str, Any]
    tags: List[str] = []
    archived: bool = False
    metadata: Optional[dict] = None

class RecallCreate(BaseModel):
    """Model for creating recall entries."""
    dispatch_id: str
    actor: str
    realm: str
    capsule: str
    intent: str
    content: Dict[str, Any]
    tags: List[str] = []
    metadata: Optional[dict] = None

class RecallQuery(BaseModel):
    """Model for querying recall entries."""
    actor: Optional[str] = None
    realm: Optional[str] = None
    capsule: Optional[str] = None
    intent: Optional[str] = None
    tags: Optional[List[str]] = []
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    archived: Optional[bool] = None

# Response Models
class StatusResponse(BaseModel):
    """Standard status response model."""
    status: str
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    detail: Optional[str] = None