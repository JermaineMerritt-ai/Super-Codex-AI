from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class ArtifactCreate(BaseModel):
    type: Literal["Constitution","Declaration","Anthem","Oath","Ceremony","Handbook","Guide","Proclamation","Compendium","Charter"]
    title: str
    slug: str
    content_uri: str

class Artifact(BaseModel):
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

class CeremonyCreate(BaseModel):
    kind: Literal["Induction","Continuum","Millennium","Opening","Closing"]
    script_ref: str
    scheduled_at: datetime
    location: str
    council_id: str

class OathRecord(BaseModel):
    ceremony_id: str
    heir_id: str
    signature: str
    recited_at: datetime