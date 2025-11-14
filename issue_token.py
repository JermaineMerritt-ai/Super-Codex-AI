#!/usr/bin/env python3
import os
import jwt
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load keys from environment
PRIMARY_KEY = os.getenv("SECRET_KEY")
SECONDARY_KEY = os.getenv("SECRET_KEY_SECONDARY")

if not PRIMARY_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
if not SECONDARY_KEY:
    raise ValueError("SECRET_KEY_SECONDARY environment variable not set")

def issue_token(user_id: str, role: str, key_choice: str = "primary", expires_minutes: int = 60):
    if key_choice == "primary":
        secret = PRIMARY_KEY
    elif key_choice == "secondary":
        secret = SECONDARY_KEY
    else:
        raise ValueError("key_choice must be 'primary' or 'secondary'")

    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codex Dominion JWT Issuer")
    parser.add_argument("--user", required=True, help="User ID (e.g., heir123)")
    parser.add_argument("--role", required=True, choices=["Heir","Council","Elder","Custodian"], help="Role claim")
    parser.add_argument("--key", default="primary", choices=["primary","secondary"], help="Which key to sign with")
    parser.add_argument("--exp", type=int, default=60, help="Expiration in minutes")
    args = parser.parse_args()

    token = issue_token(args.user, args.role, args.key, args.exp)
    print(token)