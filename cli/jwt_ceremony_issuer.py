#!/usr/bin/env python3
"""
Codex Ceremony JWT Issuer CLI
Enhanced ceremonial token issuer with role-specific ceremony types and temporal markers.
"""

import argparse
import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt

# Load environment variables
load_dotenv()

def get_secret_key(key_type):
    """Get the appropriate secret key based on key type."""
    if key_type == "primary":
        secret = os.getenv("SECRET_KEY")
        if not secret:
            raise ValueError("SECRET_KEY not found in environment variables")
        return secret
    elif key_type == "secondary":
        secret = os.getenv("SECRET_KEY_SECONDARY")
        if not secret:
            raise ValueError("SECRET_KEY_SECONDARY not found in environment variables")
        return secret
    else:
        raise ValueError("Invalid key type. Must be 'primary' or 'secondary'")

def issue_induction_token(user, ceremony_id, key_type, exp_minutes=120):
    """Issue an Heir Induction Token with specialized claims."""
    secret = get_secret_key(key_type)
    
    now = datetime.now(timezone.utc)
    exp_time = now + timedelta(minutes=exp_minutes)
    
    payload = {
        "sub": user,
        "role": "Heir",
        "ceremony": "Induction",
        "ceremony_id": ceremony_id,
        "oath_recited_at": now.isoformat(),
        "iat": int(now.timestamp()),
        "exp": int(exp_time.timestamp())
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def issue_council_token(user, ceremony_id, key_type, exp_minutes=60):
    """Issue a Council Proclamation Token with specialized claims."""
    secret = get_secret_key(key_type)
    
    now = datetime.now(timezone.utc)
    exp_time = now + timedelta(minutes=exp_minutes)
    
    payload = {
        "sub": user,
        "role": "Council",
        "ceremony": "Proclamation",
        "proclamation_id": ceremony_id,
        "quorum_verified_at": now.isoformat(),
        "iat": int(now.timestamp()),
        "exp": int(exp_time.timestamp())
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def issue_millennium_token(user, ceremony_id, key_type, exp_minutes=1440):
    """Issue an Elder Millennium Token with specialized claims."""
    secret = get_secret_key(key_type)
    
    now = datetime.now(timezone.utc)
    exp_time = now + timedelta(minutes=exp_minutes)
    
    payload = {
        "sub": user,
        "role": "Elder",
        "ceremony": "Millennium",
        "invocation_id": ceremony_id,
        "invoked_at": now.isoformat(),
        "iat": int(now.timestamp()),
        "exp": int(exp_time.timestamp())
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def main():
    parser = argparse.ArgumentParser(description="Issue ceremonial JWT tokens")
    parser.add_argument("--user", required=True, help="User identifier")
    parser.add_argument("--role", required=True, choices=["Heir", "Council", "Elder"], 
                       help="User role (determines ceremony type)")
    parser.add_argument("--ceremony_id", required=True, help="Ceremony identifier")
    parser.add_argument("--key", required=True, choices=["primary", "secondary"], 
                       help="Secret key to use for signing")
    parser.add_argument("--exp", type=int, help="Token expiration in minutes")
    
    args = parser.parse_args()
    
    try:
        # Route to appropriate ceremony function based on role
        if args.role == "Heir":
            exp_minutes = args.exp if args.exp is not None else 120
            token = issue_induction_token(args.user, args.ceremony_id, args.key, exp_minutes)
            print(f"🗡️  Heir Induction Token issued for {args.user}")
            
        elif args.role == "Council":
            exp_minutes = args.exp if args.exp is not None else 60
            token = issue_council_token(args.user, args.ceremony_id, args.key, exp_minutes)
            print(f"⚖️  Council Proclamation Token issued for {args.user}")
            
        elif args.role == "Elder":
            exp_minutes = args.exp if args.exp is not None else 1440
            token = issue_millennium_token(args.user, args.ceremony_id, args.key, exp_minutes)
            print(f"🌟 Elder Millennium Token issued for {args.user}")
        
        print(f"🔑 Key: {args.key.upper()}")
        print(f"⏱️  Expires: {exp_minutes} minutes")
        print(f"📜 Token: {token}")
        
    except Exception as e:
        print(f"❌ Error issuing token: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()