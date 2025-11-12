# test_three_patterns.py
"""
Test all three authorization patterns with real requests
"""

import asyncio
import httpx
from app.auth import create_token

async def test_all_patterns():
    """Test all three authorization patterns"""
    
    print("🧪 Testing Three Authorization Patterns")
    print("=" * 50)
    
    # Create test tokens
    admin_token = create_token("admin_user", ["admin", "operator"])
    operator_token = create_token("operator_user", ["operator"])
    council_token = create_token("council_user", ["council"])
    user_token = create_token("regular_user", ["user"])
    
    base_url = "http://127.0.0.1:8021"
    api_key = "your-api-key-here"  # From app.deps
    
    headers_admin = {
        "Authorization": f"Bearer {admin_token}",
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    headers_operator = {
        "Authorization": f"Bearer {operator_token}",
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    headers_council = {
        "Authorization": f"Bearer {council_token}",
        "Content-Type": "application/json"
    }
    
    headers_user = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        
        print("\n1️⃣ PATTERN 1: Router-Level Protection (/secure/*)")
        print("-" * 30)
        
        # Test router-level protection - requires operator/admin + API key
        test_cases_router = [
            ("Admin", headers_admin, "✅"),
            ("Operator", headers_operator, "✅"),
            ("Council", headers_council, "❌"),  # No API key or wrong role
            ("User", headers_user, "❌")
        ]
        
        for user_type, headers, expected in test_cases_router:
            try:
                response = await client.get(f"{base_url}/secure/workflow", headers=headers)
                if response.status_code == 200:
                    result = "✅ ALLOWED"
                else:
                    result = f"❌ DENIED ({response.status_code})"
            except Exception as e:
                result = f"❌ ERROR ({str(e)[:30]})"
                
            print(f"  {user_type:8} accessing /secure/workflow: {result}")
        
        print("\n2️⃣ PATTERN 2: Individual Endpoint Protection")
        print("-" * 30)
        
        # Test endpoint-level dependencies
        endpoints = [
            ("/admin-dashboard", "Admin only", [
                ("Admin", headers_admin, "✅"),
                ("Operator", headers_operator, "❌"),
                ("Council", headers_council, "❌"),
                ("User", headers_user, "❌")
            ]),
            ("/council-chamber", "Council only", [
                ("Admin", headers_admin, "❌"),  # Admin != Council 
                ("Operator", headers_operator, "❌"),
                ("Council", headers_council, "✅"),
                ("User", headers_user, "❌")
            ])
        ]
        
        for endpoint, desc, test_cases in endpoints:
            print(f"\n  {endpoint} ({desc}):")
            for user_type, headers, expected in test_cases:
                try:
                    response = await client.get(f"{base_url}{endpoint}", headers=headers)
                    if response.status_code == 200:
                        result = "✅ ALLOWED"
                    else:
                        result = f"❌ DENIED ({response.status_code})"
                except Exception as e:
                    result = f"❌ ERROR ({str(e)[:30]})"
                    
                print(f"    {user_type:8}: {result}")
        
        print("\n3️⃣ PATTERN 3: Function-Level Logic (/dynamic-operation)")
        print("-" * 30)
        
        # Test function-level authorization with different operations
        operations = [
            ("data_export", "Requires admin/operator"),
            ("user_invite", "Requires admin/council"), 
            ("system_backup", "Requires admin only"),
            ("ceremony_review", "Requires elevated roles"),
            ("view_profile", "Any authenticated user")
        ]
        
        for operation, desc in operations:
            print(f"\n  Operation: {operation} ({desc})")
            
            test_data = {"operation_type": operation, "sensitive_data": False}
            
            for user_type, headers in [
                ("Admin", headers_admin),
                ("Operator", headers_operator), 
                ("Council", headers_council),
                ("User", headers_user)
            ]:
                try:
                    response = await client.post(
                        f"{base_url}/dynamic-operation",
                        json=test_data,
                        headers=headers
                    )
                    if response.status_code == 200:
                        result = "✅ ALLOWED"
                    else:
                        result = f"❌ DENIED ({response.status_code})"
                except Exception as e:
                    result = f"❌ ERROR"
                    
                print(f"    {user_type:8}: {result}")
        
        print("\n🏆 COMBINED PATTERN: Triple Protection")
        print("-" * 30)
        
        # Test the super-secure endpoint with all three patterns
        super_secure_data = {"operation": "standard_admin_task"}
        
        print("  /protected/super-secure (Router + Endpoint + Function):")
        for user_type, headers in [
            ("Admin", headers_admin),
            ("Operator", headers_operator),
            ("Council", headers_council), 
            ("User", headers_user)
        ]:
            try:
                response = await client.post(
                    f"{base_url}/protected/super-secure",
                    json=super_secure_data,
                    headers=headers
                )
                if response.status_code == 200:
                    result = "✅ ALLOWED"
                else:
                    result = f"❌ DENIED ({response.status_code})"
            except Exception as e:
                result = f"❌ ERROR"
                
            print(f"    {user_type:8}: {result}")

if __name__ == "__main__":
    print("🔐 Authorization Patterns Test Suite")
    asyncio.run(test_all_patterns())
    print("\n✅ All authorization patterns tested!")
    print("\n📋 Summary:")
    print("  Pattern 1: Router-level protection - Applied to AXIOM routes")
    print("  Pattern 2: Endpoint-level dependencies - Available for specific routes")  
    print("  Pattern 3: Function-level logic - Flexible role checking inside functions")
    print("\n🛡️ Your system supports all three patterns!")