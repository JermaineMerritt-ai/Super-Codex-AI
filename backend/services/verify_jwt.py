import jwt
from pathlib import Path

# Load Dominion public key
PUBLIC_KEY = Path("dominion_public.pem").read_text()

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        print("✅ Token is valid")
        print("Claims:", decoded)
    except jwt.ExpiredSignatureError:
        print("❌ Token expired")
    except jwt.InvalidTokenError:
        print("❌ Invalid token")
