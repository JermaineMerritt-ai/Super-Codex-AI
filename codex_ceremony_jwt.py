#!/usr/bin/env python3
import os
import jwt
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PRIMARY_KEY = os.getenv("SECRET_KEY")
SECONDARY_KEY = os.getenv("SECRET_KEY_SECONDARY")

if not PRIMARY_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
if not SECONDARY_KEY:
    raise ValueError("SECRET_KEY_SECONDARY environment variable not set")

def _choose_key(key_choice: str):
    if key_choice == "primary":
        return PRIMARY_KEY
    elif key_choice == "secondary":
        return SECONDARY_KEY
    else:
        raise ValueError("key_choice must be 'primary' or 'secondary'")

def issue_induction_token(user_id: str, ceremony_id: str, key_choice="primary", exp_minutes=60):
    secret = _choose_key(key_choice)
    payload = {
        "sub": user_id,
        "role": "Heir",
        "ceremony": "Induction",
        "ceremony_id": ceremony_id,
        "oath_recited_at": datetime.now(timezone.utc).isoformat(),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def issue_council_token(user_id: str, proclamation_id: str, key_choice="primary", exp_minutes=60):
    secret = _choose_key(key_choice)
    payload = {
        "sub": user_id,
        "role": "Council",
        "ceremony": "Proclamation",
        "proclamation_id": proclamation_id,
        "quorum_verified_at": datetime.now(timezone.utc).isoformat(),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def issue_millennium_token(user_id: str, invocation_id: str, key_choice="primary", exp_minutes=1440):
    secret = _choose_key(key_choice)
    payload = {
        "sub": user_id,
        "role": "Elder",
        "ceremony": "Millennium",
        "invocation_id": invocation_id,
        "invoked_at": datetime.now(timezone.utc).isoformat(),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codex Ceremony JWT Issuer")
    parser.add_argument("--user", required=True, help="User ID")
    parser.add_argument("--role", required=True, choices=["Heir","Council","Elder"], help="Role")
    parser.add_argument("--ceremony_id", help="Ceremony or proclamation ID")
    parser.add_argument("--key", default="primary", choices=["primary","secondary"], help="Key choice")
    parser.add_argument("--exp", type=int, help="Expiration in minutes (default: 60 for Heir/Council, 1440 for Elder)")
    args = parser.parse_args()

    if args.role == "Heir":
        exp_minutes = args.exp if args.exp is not None else 60
        token = issue_induction_token(args.user, args.ceremony_id, args.key, exp_minutes)
    elif args.role == "Council":
        exp_minutes = args.exp if args.exp is not None else 60
        token = issue_council_token(args.user, args.ceremony_id, args.key, exp_minutes)
    elif args.role == "Elder":
        exp_minutes = args.exp if args.exp is not None else 1440
        token = issue_millennium_token(args.user, args.ceremony_id, args.key, exp_minutes)
    else:
        raise ValueError("Unsupported role")

    print(token)