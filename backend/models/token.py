from pydantic import BaseModel
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

class DominionToken(BaseModel):
    token_id: str
    email: str
    role: str
    order_id: str
    issued_at: datetime


@dataclass
class RefreshToken:
    id: int
    email: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool = False

    @classmethod
    def create(cls, id: int, email: str, lifetime_minutes: int = 60):
        now = datetime.now(timezone.utc)
        return cls(id=id, email=email, issued_at=now, expires_at=now + timedelta(minutes=lifetime_minutes))
