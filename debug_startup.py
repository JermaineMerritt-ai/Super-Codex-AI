#!/usr/bin/env python3
"""
Debug startup script to identify and fix AXIOM-FLAME API issues.
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test all critical imports."""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI version: {fastapi.__version__}")
    except Exception as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
        
    try:
        import uvicorn
        print(f"✅ Uvicorn available")
    except Exception as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
        
    try:
        import pydantic
        print(f"✅ Pydantic version: {pydantic.VERSION}")
    except Exception as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
        
    try:
        from app.models import GovernanceRule, Identity, RecallEntry
        print("✅ All models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        traceback.print_exc()
        return False
        
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """Test FastAPI app creation."""
    print("\n🔍 Testing app creation...")
    
    try:
        from app.main import app
        print(f"✅ App created: {type(app)}")
        print(f"✅ App title: {app.title}")
        print(f"✅ Available routes: {len(app.routes)}")
        for route in app.routes:
            if hasattr(route, 'path'):
                print(f"  - {route.path}")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return False

def test_models():
    """Test model creation."""
    print("\n🔍 Testing model instantiation...")
    
    try:
        from app.models import GovernanceRule, GovernanceRuleCreate
        from datetime import datetime
        
        # Test model creation
        rule_data = GovernanceRuleCreate(
            name="Test Rule",
            description="Test Description",
            authority_level="Standard",
            seal_type="Sacred"
        )
        print(f"✅ GovernanceRuleCreate: {rule_data}")
        
        rule = GovernanceRule(
            id="test-1",
            name="Test Rule",
            description="Test Description", 
            authority_level="Standard",
            seal_type="Sacred",
            created_at=datetime.now()
        )
        print(f"✅ GovernanceRule: {rule}")
        return True
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function."""
    print("🚀 AXIOM-FLAME API Diagnostic Tool")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Exiting.")
        sys.exit(1)
    
    # Test app creation  
    if not test_app_creation():
        print("\n❌ App creation failed. Exiting.")
        sys.exit(1)
        
    # Test models
    if not test_models():
        print("\n❌ Model tests failed. Exiting.")
        sys.exit(1)
    
    print("\n✅ All diagnostic tests passed!")
    print("🚀 Attempting to start server...")
    
    try:
        import uvicorn
        from app.main import app
        
        print("Starting server on http://0.0.0.0:8080")
        uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server startup failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()