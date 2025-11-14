#!/usr/bin/env python3
import os
import jwt
import argparse
from datetime import datetime, timezone
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

def verify_token(token: str):
    """Verify a JWT token using both primary and secondary keys (dual-key fallback)"""
    
    # Try primary key first
    try:
        payload = jwt.decode(token, PRIMARY_KEY, algorithms=["HS256"])
        print("✅ Token verified with PRIMARY key")
        return payload, "primary"
    except jwt.InvalidTokenError as e:
        print(f"❌ Primary key verification failed: {e}")
    
    # Try secondary key as fallback
    try:
        payload = jwt.decode(token, SECONDARY_KEY, algorithms=["HS256"])
        print("✅ Token verified with SECONDARY key")
        return payload, "secondary"
    except jwt.InvalidTokenError as e:
        print(f"❌ Secondary key verification failed: {e}")
        raise jwt.InvalidTokenError("Token verification failed with both keys")

def format_timestamp(timestamp):
    """Format Unix timestamp to readable datetime"""
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return "N/A"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codex Dominion JWT Verifier")
    parser.add_argument("token", help="JWT token to verify")
    parser.add_argument("--decode-only", action="store_true", help="Decode without verification (unsafe)")
    args = parser.parse_args()

    try:
        if args.decode_only:
            # Decode without verification (for debugging expired tokens)
            payload = jwt.decode(args.token, options={"verify_signature": False})
            key_used = "none (unverified)"
        else:
            # Verify token with dual-key fallback
            payload, key_used = verify_token(args.token)
        
        print(f"\n📋 Token Details:")
        print(f"   Subject (sub): {payload.get('sub', 'N/A')}")
        print(f"   Role: {payload.get('role', 'N/A')}")
        print(f"   Issued At: {format_timestamp(payload.get('iat'))}")
        print(f"   Expires At: {format_timestamp(payload.get('exp'))}")
        print(f"   Key Used: {key_used}")
        
        # Check if token is expired
        if payload.get('exp'):
            exp_time = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
            now = datetime.now(timezone.utc)
            if now > exp_time:
                print(f"   Status: ⚠️  EXPIRED ({(now - exp_time).total_seconds():.0f} seconds ago)")
            else:
                print(f"   Status: ✅ VALID (expires in {(exp_time - now).total_seconds():.0f} seconds)")
        
    except jwt.InvalidTokenError as e:
        print(f"❌ Token verification failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")