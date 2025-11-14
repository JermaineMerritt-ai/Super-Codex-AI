"""
Council Access Crown - Authorization and access management system
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json

class AccessLevel(Enum):
    GUEST = "guest"
    MEMBER = "member"
    COUNCIL = "council"
    CUSTODIAN = "custodian"
    SOVEREIGN = "sovereign"

class RealmType(Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    CEREMONIAL = "ceremonial"
    SOVEREIGN = "sovereign"

@dataclass
class AccessGrant:
    user_id: str
    realm_id: str
    access_level: AccessLevel
    granted_by: str
    granted_date: datetime
    expires_date: Optional[datetime] = None
    active: bool = True

class CouncilAccessCrownManager:
    def __init__(self):
        self.access_grants: Dict[str, AccessGrant] = {}
        self.realms: Dict[str, Dict[str, Any]] = {}
        
    def grant_access(self, user_id: str, realm_id: str, access_level: AccessLevel, 
                    granted_by: str, expires_date: Optional[datetime] = None) -> str:
        grant_id = f"AG-{datetime.now().strftime('%Y%m%d')}-{len(self.access_grants)+1:04d}"
        
        grant = AccessGrant(
            user_id=user_id,
            realm_id=realm_id,
            access_level=access_level,
            granted_by=granted_by,
            granted_date=datetime.now(),
            expires_date=expires_date
        )
        
        self.access_grants[grant_id] = grant
        return grant_id
        
    def check_access(self, user_id: str, realm_id: str, required_level: AccessLevel) -> bool:
        user_grants = [g for g in self.access_grants.values() 
                      if g.user_id == user_id and g.realm_id == realm_id and g.active]
        
        if not user_grants:
            return False
            
        # Check if any grant provides sufficient access
        for grant in user_grants:
            if self._has_sufficient_access(grant.access_level, required_level):
                # Check expiration
                if grant.expires_date and grant.expires_date < datetime.now():
                    continue
                return True
                
        return False
        
    def _has_sufficient_access(self, user_level: AccessLevel, required_level: AccessLevel) -> bool:
        access_hierarchy = {
            AccessLevel.GUEST: 1,
            AccessLevel.MEMBER: 2, 
            AccessLevel.COUNCIL: 3,
            AccessLevel.CUSTODIAN: 4,
            AccessLevel.SOVEREIGN: 5
        }
        
        return access_hierarchy.get(user_level, 0) >= access_hierarchy.get(required_level, 0)
        
    def revoke_access(self, grant_id: str, revoked_by: str) -> bool:
        if grant_id in self.access_grants:
            self.access_grants[grant_id].active = False
            return True
        return False
        
    def list_user_access(self, user_id: str) -> List[AccessGrant]:
        return [g for g in self.access_grants.values() if g.user_id == user_id and g.active]