from ..models.user import User


def get_user_by_email(email: str) -> User:
    if email == 'council@example.com':
        return User(id=1, email=email, role='council')
    return User(id=2, email=email, role='custodian')
