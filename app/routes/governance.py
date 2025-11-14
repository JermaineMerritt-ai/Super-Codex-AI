from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from app.models import GovernanceRule, GovernanceRuleCreate, Council, CouncilCreate

router = APIRouter()

# In-memory storage for demo purposes
governance_rules_db = {}
councils_db = {}

@router.get("/rules", response_model=List[GovernanceRule])
async def list_governance_rules():
    """List all governance rules"""
    return list(governance_rules_db.values())

@router.get("/rules/{rule_id}", response_model=GovernanceRule)
async def get_governance_rule(rule_id: str):
    """Get a specific governance rule by ID"""
    if rule_id not in governance_rules_db:
        raise HTTPException(status_code=404, detail="Governance rule not found")
    return governance_rules_db[rule_id]

@router.post("/rules", response_model=GovernanceRule)
async def create_governance_rule(rule: GovernanceRuleCreate):
    """Create a new governance rule"""
    rule_id = f"gov_{len(governance_rules_db) + 1}"
    
    new_rule = GovernanceRule(
        id=rule_id,
        name=rule.name,
        description=rule.description,
        authority_level=rule.authority_level,
        seal_type=rule.seal_type,
        created_at=datetime.now(),
        metadata=rule.metadata
    )
    governance_rules_db[rule_id] = new_rule
    return new_rule

@router.get("/councils", response_model=List[Council])
async def list_councils():
    """List all councils"""
    return list(councils_db.values())

@router.get("/councils/{council_id}", response_model=Council)
async def get_council(council_id: str):
    """Get a specific council by ID"""
    if council_id not in councils_db:
        raise HTTPException(status_code=404, detail="Council not found")
    return councils_db[council_id]

@router.post("/councils", response_model=Council)
async def create_council(council: CouncilCreate):
    """Create a new council"""
    council_id = f"council_{len(councils_db) + 1}"
    
    new_council = Council(
        id=council_id,
        name=council.name,
        members=council.members,
        authority_level=council.authority_level,
        created_at=datetime.now()
    )
    councils_db[council_id] = new_council
    return new_council

@router.get("/seals")
async def list_seal_types():
    """List available seal types"""
    return {
        "seal_types": [
            {"name": "Sacred", "authority": "High", "description": "Sacred ceremonial seal"},
            {"name": "Eternal", "authority": "Maximum", "description": "Eternal governance seal"},
            {"name": "Council", "authority": "Medium", "description": "Council authorization seal"},
            {"name": "Custodian", "authority": "Standard", "description": "Custodian operational seal"}
        ]
    }

@router.get("/status")
async def governance_status():
    """Get governance system status"""
    return {
        "status": "active",
        "rules_count": len(governance_rules_db),
        "councils_count": len(councils_db),
        "authority_levels": ["Standard", "Medium", "High", "Maximum"],
        "timestamp": datetime.now().isoformat()
    }
