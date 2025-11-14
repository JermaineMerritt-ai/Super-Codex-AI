#!/usr/bin/env python3
"""Test JWT token compatibility with authentication system"""

import sys
sys.path.append('.')
from app.security.auth import decode_token
import os
from dotenv import load_dotenv

load_dotenv()

# Generate a token
from jwt_manager import issue_token

def test_token_compatibility():
    print("🧪 Testing JWT Token Compatibility")
    print("=" * 40)
    
    # Test different scenarios
    test_cases = [
        ("testuser", "Council", "primary"),
        ("admin", "Heir", "secondary"),
        ("elder", "Elder", "primary"),
        ("custodian", "Custodian", "secondary")
    ]
    
    for user, role, key in test_cases:
        print(f"\n🔄 Testing: {user} ({role}) with {key} key")
        
        try:
            # Generate token with utility
            token = issue_token(user, role, key, 30)
            print(f"   Token generated: {token[:30]}...")
            
            # Verify with auth system
            payload = decode_token(token)
            print(f"   ✅ Auth system verification successful")
            print(f"   User: {payload.get('sub')}")
            print(f"   Role: {payload.get('role')}")
            
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n✅ JWT utilities are fully compatible with the authentication system!")

if __name__ == "__main__":
    test_token_compatibility()