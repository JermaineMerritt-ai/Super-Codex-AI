from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str
    role: str = "custodian"


def is_council(user: User) -> bool:
    return user and user.role == 'council'
