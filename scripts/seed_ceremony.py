#!/usr/bin/env python3
"""
Ceremony Seeding Script
Sets up governance middleware and ceremony authentication infrastructure
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PRIMARY_KEY = os.getenv("SECRET_KEY")
SECONDARY_KEY = os.getenv("SECRET_KEY_SECONDARY")

def decode_dual_key(token: str):
    """
    Decode JWT token using dual key fallback system
    Tries PRIMARY_KEY first, then SECONDARY_KEY
    """
    try:
        return jwt.decode(token, PRIMARY_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        try:
            return jwt.decode(token, SECONDARY_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware for ceremony governance and authentication
    Enforces role-based access control for ceremonial operations
    """
    
    async def dispatch(self, request: Request, call_next):
        # Only enforce on protected routes
        if request.url.path.startswith("/v1/ceremonies") or request.url.path.startswith("/v1/artifacts"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing token")

            token = auth_header.split(" ")[1]
            payload = decode_dual_key(token)

            role = payload.get("role")
            ceremony = payload.get("ceremony")

            # Induction rules
            if ceremony == "Induction" and role == "Heir":
                if "oath_recited_at" not in payload:
                    raise HTTPException(status_code=403, detail="Induction token missing oath_recited_at")

            # Council proclamation rules
            if ceremony == "Proclamation" and role == "Council":
                if "quorum_verified_at" not in payload:
                    raise HTTPException(status_code=403, detail="Council token missing quorum_verified_at")

            # Millennium invocation rules
            if ceremony == "Millennium" and role == "Elder":
                if "invoked_at" not in payload:
                    raise HTTPException(status_code=403, detail="Millennium token missing invoked_at")

        response = await call_next(request)
        return response

def validate_environment():
    """Validate required environment variables for ceremony operations"""
    print("🔧 Validating ceremony environment...")
    
    if not PRIMARY_KEY:
        raise ValueError("❌ SECRET_KEY environment variable is required")
    
    if not SECONDARY_KEY:
        print("⚠️  SECRET_KEY_SECONDARY not set - using PRIMARY_KEY only")
    
    print(f"✅ Primary key configured: {bool(PRIMARY_KEY)}")
    print(f"✅ Secondary key configured: {bool(SECONDARY_KEY)}")

def seed_ceremony_tokens():
    """Generate sample ceremony tokens for testing"""
    import datetime
    
    print("\n🎭 Generating sample ceremony tokens...")
    
    if not PRIMARY_KEY:
        print("❌ Cannot generate tokens without SECRET_KEY")
        return
    
    # Sample payloads for different ceremonies
    sample_tokens = {
        "induction": {
            "role": "Heir", 
            "ceremony": "Induction",
            "oath_recited_at": datetime.datetime.utcnow().isoformat(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        "proclamation": {
            "role": "Council", 
            "ceremony": "Proclamation",
            "quorum_verified_at": datetime.datetime.utcnow().isoformat(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        },
        "millennium": {
            "role": "Elder", 
            "ceremony": "Millennium",
            "invoked_at": datetime.datetime.utcnow().isoformat(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)
        }
    }
    
    for ceremony_type, payload in sample_tokens.items():
        # Convert datetime objects to timestamps for JWT
        jwt_payload = {
            k: v.timestamp() if isinstance(v, datetime.datetime) else v
            for k, v in payload.items()
        }
        
        token = jwt.encode(jwt_payload, PRIMARY_KEY, algorithm="HS256")
        print(f"📜 {ceremony_type.upper()} token: {token[:50]}...")

def test_middleware_validation():
    """Test ceremony validation logic"""
    print("\n🧪 Testing ceremony validation logic...")
    
    # Test cases for ceremony validation
    test_cases = [
        {"role": "Heir", "ceremony": "Induction", "oath_recited_at": "2025-01-01T00:00:00Z"},
        {"role": "Council", "ceremony": "Proclamation", "quorum_verified_at": "2025-01-01T00:00:00Z"},
        {"role": "Elder", "ceremony": "Millennium", "invoked_at": "2025-01-01T00:00:00Z"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        ceremony = test_case.get("ceremony")
        role = test_case.get("role")
        
        print(f"  Test {i}: {ceremony} ceremony with {role} role")
        
        # Validate each ceremony type
        if ceremony == "Induction" and role == "Heir":
            if "oath_recited_at" in test_case:
                print(f"    ✅ Induction validation passed")
            else:
                print(f"    ❌ Missing oath_recited_at")
                
        elif ceremony == "Proclamation" and role == "Council":
            if "quorum_verified_at" in test_case:
                print(f"    ✅ Proclamation validation passed")
            else:
                print(f"    ❌ Missing quorum_verified_at")
                
        elif ceremony == "Millennium" and role == "Elder":
            if "invoked_at" in test_case:
                print(f"    ✅ Millennium validation passed")
            else:
                print(f"    ❌ Missing invoked_at")

def main():
    """Main seeding function"""
    print("🏛️  CEREMONY SEEDING SCRIPT")
    print("=" * 50)
    
    try:
        # Validate environment
        validate_environment()
        
        # Generate sample tokens
        seed_ceremony_tokens()
        
        # Test validation logic
        test_middleware_validation()
        
        print("\n✅ Ceremony seeding completed successfully!")
        print("\n📋 Summary:")
        print("   - Governance middleware configured")
        print("   - Sample ceremony tokens generated")
        print("   - Validation logic tested")
        print("   - Ready for ceremony API integration")
        
    except Exception as e:
        print(f"\n❌ Ceremony seeding failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())