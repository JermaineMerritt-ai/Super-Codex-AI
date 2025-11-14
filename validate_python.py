#!/usr/bin/env python3
"""
Comprehensive Python system validation for AXIOM-FLAME API.
Tests all Python components without external dependencies.
"""

import sys
import traceback
import json
from datetime import datetime
from pathlib import Path

def test_python_version():
    """Test Python version compatibility."""
    print("🔍 Testing Python version...")
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version may have compatibility issues")
        return False

def test_all_imports():
    """Test all critical imports."""
    print("\n🔍 Testing all imports...")
    
    imports = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("datetime", "datetime"),
        ("json", "JSON"),
        ("pathlib", "pathlib"),
        ("uuid", "UUID"),
        ("typing", "typing"),
    ]
    
    success_count = 0
    for module, name in imports:
        try:
            __import__(module)
            print(f"✅ {name}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: {e}")
    
    print(f"📊 Import success: {success_count}/{len(imports)}")
    return success_count == len(imports)

def test_models():
    """Test all model classes."""
    print("\n🔍 Testing model classes...")
    
    try:
        from app.models import (
            GovernanceRule, GovernanceRuleCreate, Council, CouncilCreate,
            Identity, IdentityCreate, AuthRequest, Token,
            RecallEntry, RecallCreate, RecallQuery,
            Artifact, ArtifactCreate,
            Ceremony, CeremonyCreate, OathRecord
        )
        
        models = [
            ("GovernanceRule", GovernanceRule),
            ("GovernanceRuleCreate", GovernanceRuleCreate),
            ("Council", Council),
            ("CouncilCreate", CouncilCreate),
            ("Identity", Identity),
            ("IdentityCreate", IdentityCreate),
            ("AuthRequest", AuthRequest),
            ("Token", Token),
            ("RecallEntry", RecallEntry),
            ("RecallCreate", RecallCreate),
            ("RecallQuery", RecallQuery),
            ("Artifact", Artifact),
            ("ArtifactCreate", ArtifactCreate),
            ("Ceremony", Ceremony),
            ("CeremonyCreate", CeremonyCreate),
            ("OathRecord", OathRecord),
        ]
        
        success_count = 0
        for name, model_class in models:
            try:
                # Check if model has required fields
                if hasattr(model_class, '__annotations__'):
                    print(f"✅ {name}: {len(model_class.__annotations__)} fields")
                    success_count += 1
                else:
                    print(f"❌ {name}: No annotations found")
            except Exception as e:
                print(f"❌ {name}: {e}")
        
        print(f"📊 Model success: {success_count}/{len(models)}")
        return success_count == len(models)
        
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        traceback.print_exc()
        return False

def test_route_modules():
    """Test all route modules."""
    print("\n🔍 Testing route modules...")
    
    routes = [
        ("artifacts", "app.routes.artifacts"),
        ("ceremonies", "app.routes.ceremonies"),
        ("governance", "app.routes.governance"),
        ("identity", "app.routes.identity"),
        ("recall", "app.routes.recall"),
    ]
    
    success_count = 0
    for name, module_path in routes:
        try:
            module = __import__(module_path, fromlist=[name])
            if hasattr(module, 'router'):
                route_count = len(module.router.routes)
                print(f"✅ {name}: {route_count} routes")
                success_count += 1
            else:
                print(f"❌ {name}: No router found")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    print(f"📊 Route success: {success_count}/{len(routes)}")
    return success_count == len(routes)

def test_fastapi_app():
    """Test FastAPI application creation."""
    print("\n🔍 Testing FastAPI application...")
    
    try:
        from app.main import app
        
        print(f"✅ App created: {app.title}")
        print(f"✅ Version: {app.version}")
        print(f"✅ Routes: {len(app.routes)}")
        
        # Test that all routes are properly registered
        route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        expected_prefixes = ['/v1/artifacts', '/v1/ceremonies', '/v1/governance', '/v1/identity', '/v1/recall']
        
        found_prefixes = []
        for prefix in expected_prefixes:
            if any(path.startswith(prefix) for path in route_paths):
                found_prefixes.append(prefix)
                print(f"✅ {prefix} routes registered")
            else:
                print(f"❌ {prefix} routes missing")
        
        success = len(found_prefixes) == len(expected_prefixes)
        print(f"📊 Route prefix success: {len(found_prefixes)}/{len(expected_prefixes)}")
        return success
        
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        traceback.print_exc()
        return False

def test_model_serialization():
    """Test model serialization."""
    print("\n🔍 Testing model serialization...")
    
    try:
        from app.models import GovernanceRuleCreate, IdentityCreate, RecallCreate
        
        # Test GovernanceRuleCreate
        rule = GovernanceRuleCreate(
            name="Test Rule",
            description="Test Description",
            authority_level="Standard",
            seal_type="Sacred"
        )
        rule_dict = rule.model_dump()
        print(f"✅ GovernanceRuleCreate serialization: {len(rule_dict)} fields")
        
        # Test IdentityCreate
        identity = IdentityCreate(
            actor="TestActor",
            realm="TestRealm",
            authority_level="Standard",
            capsules=["cap1", "cap2"]
        )
        identity_dict = identity.model_dump()
        print(f"✅ IdentityCreate serialization: {len(identity_dict)} fields")
        
        # Test RecallCreate
        recall = RecallCreate(
            dispatch_id="test-123",
            actor="TestActor",
            realm="TestRealm",
            capsule="TestCapsule",
            intent="TestIntent",
            content={"test": "data"}
        )
        recall_dict = recall.model_dump()
        print(f"✅ RecallCreate serialization: {len(recall_dict)} fields")
        
        print("✅ All model serialization tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Model serialization failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🐍 AXIOM-FLAME Python System Validation")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Imports", test_all_imports),
        ("Models", test_models),
        ("Routes", test_route_modules),
        ("FastAPI App", test_fastapi_app),
        ("Serialization", test_model_serialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 Final Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All Python components are working correctly!")
        print("🚀 Ready to start AXIOM-FLAME API server")
        return 0
    else:
        print("⚠️  Some issues found. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())