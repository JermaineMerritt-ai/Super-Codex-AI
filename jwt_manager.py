#!/usr/bin/env python3
"""
Codex Dominion JWT Management Utility

This script provides comprehensive JWT token management for the Super-Codex-AI system,
including token generation, verification, and analysis.
"""

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
    """Issue a new JWT token"""
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

def verify_token(token: str, decode_only: bool = False):
    """Verify a JWT token using dual-key fallback"""
    
    if decode_only:
        # Decode without verification (for debugging)
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload, "none (unverified)"
    
    # Try primary key first
    try:
        payload = jwt.decode(token, PRIMARY_KEY, algorithms=["HS256"])
        return payload, "primary"
    except jwt.InvalidTokenError:
        pass
    
    # Try secondary key as fallback
    try:
        payload = jwt.decode(token, SECONDARY_KEY, algorithms=["HS256"])
        return payload, "secondary"
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Token verification failed with both keys")

def format_timestamp(timestamp):
    """Format Unix timestamp to readable datetime"""
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return "N/A"

def print_token_details(payload, key_used):
    """Print formatted token details"""
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

def main():
    parser = argparse.ArgumentParser(
        description="Codex Dominion JWT Management Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Issue a new token
  %(prog)s issue --user admin --role Heir --exp 60

  # Verify a token
  %(prog)s verify eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

  # Decode token without verification (for debugging)
  %(prog)s verify --decode-only eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Issue token subcommand
    issue_parser = subparsers.add_parser('issue', help='Issue a new JWT token')
    issue_parser.add_argument("--user", required=True, help="User ID (e.g., heir123)")
    issue_parser.add_argument("--role", required=True, choices=["Heir","Council","Elder","Custodian"], help="Role claim")
    issue_parser.add_argument("--key", default="primary", choices=["primary","secondary"], help="Which key to sign with")
    issue_parser.add_argument("--exp", type=int, default=60, help="Expiration in minutes")
    issue_parser.add_argument("--verify", action="store_true", help="Verify the issued token immediately")
    
    # Verify token subcommand
    verify_parser = subparsers.add_parser('verify', help='Verify an existing JWT token')
    verify_parser.add_argument("token", help="JWT token to verify")
    verify_parser.add_argument("--decode-only", action="store_true", help="Decode without verification (unsafe)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'issue':
            # Issue new token
            token = issue_token(args.user, args.role, args.key, args.exp)
            print(f"✅ Token issued successfully:")
            print(token)
            
            if args.verify:
                # Immediately verify the issued token
                print(f"\n🔍 Verifying issued token...")
                payload, key_used = verify_token(token)
                print(f"✅ Token verified with {key_used.upper()} key")
                print_token_details(payload, key_used)
        
        elif args.command == 'verify':
            # Verify existing token
            payload, key_used = verify_token(args.token, args.decode_only)
            if not args.decode_only:
                print(f"✅ Token verified with {key_used.upper()} key")
            print_token_details(payload, key_used)
    
    except jwt.InvalidTokenError as e:
        print(f"❌ Token verification failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()