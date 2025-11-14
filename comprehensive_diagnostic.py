#!/usr/bin/env python3
"""
Comprehensive diagnostic script to identify all issues in the Super-Codex-AI project.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

def test_environment():
    """Test environment variables and configuration."""
    print("🔍 Testing Environment Configuration...")
    
    required_vars = [
        'SECRET_KEY', 
        'SECRET_KEY_SECONDARY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables present")
        return True

def test_imports():
    """Test all module imports."""
    print("\n🔍 Testing Module Imports...")
    
    modules = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'jwt',
        'app.main',
        'app.models',
        'app.routes.artifacts',
        'app.routes.ceremonies',
        'app.routes.governance',
        'app.routes.identity',
        'app.routes.recall',
        'app.routers.authentication',
        'app.security.auth'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
            failed_imports.append((module, str(e)))
    
    return len(failed_imports) == 0

def test_model_consistency():
    """Test that all models are properly defined and consistent."""
    print("\n🔍 Testing Model Consistency...")
    
    try:
        from app.models import (
            ArtifactCreate, Artifact,
            CeremonyCreate, Ceremony, OathRecord,
            GovernanceRule, GovernanceRuleCreate, Council, CouncilCreate, 
            Identity, IdentityCreate, AuthRequest, Token,
            RecallEntry, RecallCreate, RecallQuery
        )
        
        # Test basic model instantiation
        artifact_create = ArtifactCreate(
            type="Constitution",
            title="Test Constitution",
            slug="test-constitution",
            content_uri="test://content"
        )
        
        ceremony_create = CeremonyCreate(
            kind="Induction",
            script_ref="test-script",
            scheduled_at="2024-01-01T12:00:00",
            location="Test Location",
            council_id="test-council"
        )
        
        print("✅ All models import and instantiate correctly")
        return True
        
    except Exception as e:
        print(f"❌ Model consistency error: {e}")
        traceback.print_exc()
        return False

def test_route_consistency():
    """Test that all routes can be imported and have proper routers."""
    print("\n🔍 Testing Route Consistency...")
    
    routes = [
        'app.routes.artifacts',
        'app.routes.ceremonies',
        'app.routes.governance',
        'app.routes.identity',
        'app.routes.recall'
    ]
    
    failed_routes = []
    
    for route_module in routes:
        try:
            module = importlib.import_module(route_module)
            if not hasattr(module, 'router'):
                failed_routes.append(f"{route_module}: No 'router' attribute")
            else:
                print(f"✅ {route_module}")
        except Exception as e:
            failed_routes.append(f"{route_module}: {e}")
            print(f"❌ {route_module}: {e}")
    
    return len(failed_routes) == 0

def test_authentication_system():
    """Test the authentication system."""
    print("\n🔍 Testing Authentication System...")
    
    try:
        from app.security.auth import decode_token, get_current_user
        from app.routers.authentication import router
        
        # Test that auth dependencies work (basic structure test)
        print("✅ Authentication modules load correctly")
        
        # Test JWT functionality
        import jwt
        test_payload = {"user_id": "test", "role": "admin"}
        secret_key = os.getenv("SECRET_KEY")
        
        if secret_key:
            token = jwt.encode(test_payload, secret_key, algorithm="HS256")
            decoded = decode_token(token)
            print("✅ JWT encoding/decoding works")
        else:
            print("⚠️  Cannot test JWT without SECRET_KEY")
            
        return True
        
    except Exception as e:
        print(f"❌ Authentication system error: {e}")
        traceback.print_exc()
        return False

def test_application_assembly():
    """Test that the main application can be assembled."""
    print("\n🔍 Testing Application Assembly...")
    
    try:
        from fastapi import FastAPI
        from app.routes import artifacts, ceremonies, governance, identity, recall
        from app.routers import authentication
        
        # Create a test app
        app = FastAPI(title="Test AXIOM-FLAME API")
        
        # Include all routers
        app.include_router(artifacts.router, prefix="/v1/artifacts", tags=["artifacts"])
        app.include_router(ceremonies.router, prefix="/v1/ceremonies", tags=["ceremonies"])
        app.include_router(governance.router, prefix="/v1/governance", tags=["governance"])
        app.include_router(identity.router, prefix="/v1/identity", tags=["identity"])
        app.include_router(recall.router, prefix="/v1/recall", tags=["recall"])
        app.include_router(authentication.router, prefix="/v1")
        
        print("✅ Application assembly successful")
        return True
        
    except Exception as e:
        print(f"❌ Application assembly error: {e}")
        traceback.print_exc()
        return False

def test_file_permissions():
    """Test file permissions and accessibility."""
    print("\n🔍 Testing File Permissions...")
    
    important_files = [
        'app/__init__.py',
        'app/main.py',
        'app/models.py',
        'app/routes/__init__.py',
        'app/security/__init__.py',
        'app/routers/__init__.py',
        '.env'
    ]
    
    issues = []
    
    for file_path in important_files:
        full_path = Path(file_path)
        if not full_path.exists():
            issues.append(f"Missing file: {file_path}")
        elif not full_path.is_file():
            issues.append(f"Not a file: {file_path}")
        elif not os.access(full_path, os.R_OK):
            issues.append(f"Cannot read: {file_path}")
        else:
            print(f"✅ {file_path}")
    
    if issues:
        for issue in issues:
            print(f"❌ {issue}")
        return False
    
    return True

def main():
    """Run all diagnostic tests."""
    print("🚀 Super-Codex-AI Comprehensive Diagnostic")
    print("=" * 50)
    
    tests = [
        test_file_permissions,
        test_environment,
        test_imports,
        test_model_consistency,
        test_route_consistency,
        test_authentication_system,
        test_application_assembly
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ System appears to be fully functional!")
    else:
        print(f"⚠️  TESTS PASSED: {passed}/{total}")
        print(f"❌ {total - passed} issues need to be resolved")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)