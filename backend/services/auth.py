from ..models.user import User
from council_access_crown import (
    CouncilAccessCrownManager, SovereignMode, AccessLevel, 
    ParticipantIdentity, ParticipantCredentials, Participant, RealmAccess
)


def get_user_by_email(email: str) -> User:
    if email == 'council@example.com':
        return User(id=1, email=email, role='council')
    return User(id=2, email=email, role='custodian')


def create_access_crown_for_user(user: User, realm_id: str = "PL-001"):
    """Create a Council Access Crown for a user based on their role"""
    manager = CouncilAccessCrownManager()
    
    # Create participant identity
    identity = ParticipantIdentity(
        name=user.email.split('@')[0].title(),
        email=user.email
    )
    
    credentials = ParticipantCredentials(
        auth_tokens=[f"token_{user.id}"]
    )
    
    participant = Participant(
        id=f"USER-{user.id:03d}",
        identity=identity,
        credentials=credentials
    )
    
    # Create realm access
    realm = RealmAccess(
        realm_id=realm_id,
        domain="codexdominion.app",
        access_level=AccessLevel.COUNCIL if user.role == 'council' else AccessLevel.CUSTODIAN
    )
    
    # Create appropriate crown based on role
    if user.role == 'council':
        return manager.create_council_crown(
            participant=participant,
            realm=realm,
            administrative_realms=[realm_id]
        )
    elif user.role == 'custodian':
        # Treat custodians as heirs with stewardship privileges
        return manager.create_heir_crown(
            participant=participant,
            realm=realm,
            inheritance_claims=["custodial_duties", "stewardship_seals"]
        )
    else:
        return manager.create_customer_crown(
            participant=participant,
            realm=realm,
            service_tiers=["basic_access"]
        )


def verify_user_access(user: User, resource: str, action: str, realm_id: str = "PL-001") -> bool:
    """Verify user access using Council Access Crown system"""
    crown = create_access_crown_for_user(user, realm_id)
    manager = CouncilAccessCrownManager()
    return manager.verify_access(crown, resource, action)
