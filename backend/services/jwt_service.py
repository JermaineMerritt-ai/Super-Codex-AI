PUBLIC_KEY = Path("dominion_public.pem").read_text()

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
import jwt
import datetime
from pathlib import Path

PRIVATE_KEY = Path("dominion_private.pem").read_text()

def issue_signed_token(email: str, role: str, order_id: str):
    payload = {
        "sub": email,
        "role": role,
        "order_id": order_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)  # 1 year validity
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token
