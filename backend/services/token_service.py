import uuid
from datetime import datetime
from .ledger import log_token_event
from models.token import DominionToken

def issue_token(email: str, role: str, order_id: str) -> DominionToken:
    token = DominionToken(
        token_id=str(uuid.uuid4()),
        email=email,
        role=role,
        order_id=order_id,
        issued_at=datetime.utcnow()
    )

    # Log into Dominion ledger
    log_token_event(token)

    return token
