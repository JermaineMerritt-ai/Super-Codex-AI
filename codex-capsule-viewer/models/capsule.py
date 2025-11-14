from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Capsule(BaseModel):
    id: str
    title: str
    sigil: str
    createdAt: datetime
    content: Optional[str] = None
    heirRights: Optional[List[str]] = None
    covenantSeals: Optional[List[str]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CapsuleCreate(BaseModel):
    title: str
    sigil: str
    content: Optional[str] = None
    heirRights: Optional[List[str]] = None

class CapsuleResponse(BaseModel):
    id: str
    title: str
    sigil: str
    createdAt: datetime
    summary: Optional[str] = None