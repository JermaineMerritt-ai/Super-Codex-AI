from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    role: str = "custodian"
    sovereign_mode: Optional[str] = None  # heir, council, customer
    inheritance_tier: Optional[str] = None  # initiate, steward, custodian, council, sovereign
    access_crown_id: Optional[str] = None  # Link to Council Access Crown


def is_council(user: User) -> bool:
    """Check if user has council privileges in the luminous covenant"""
    return user and (user.role == 'council' or user.sovereign_mode == 'council')


def is_heir(user: User) -> bool:
    """Check if user has heir privileges - inheriting in witness"""
    return user and (user.sovereign_mode == 'heir' or user.role == 'custodian')


def is_customer(user: User) -> bool:
    """Check if user partakes in luminous service"""
    return user and (user.sovereign_mode == 'customer' or user.role not in ['council', 'custodian'])


def get_sovereign_mode(user: User) -> str:
    """Determine the sovereign mode for a user in the three-mode hierarchy"""
    if user.sovereign_mode:
        return user.sovereign_mode
    elif user.role == 'council':
        return 'council'
    elif user.role == 'custodian':
        return 'heir'
    else:
        return 'customer'
