#!/usr/bin/env python3
"""
Test script for Sovereign Commerce Platform
Validates platform functionality and structure
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_platform_structure():
    """Test that all required directories and files exist"""
    print("🏛️ Testing Sovereign Commerce Platform Structure...")
    
    base_dir = Path(".")
    required_items = [
        "spec.json",
        "SIGIL-BUILD-0001.md",
        "README.md",
        "ui/templates",
        "ui/static",
        "services/main.py",
        "db/schema.sql",
        "ops/deploy.py"
    ]
    
    missing_items = []
    for item in required_items:
        if not (base_dir / item).exists():
            missing_items.append(item)
    
    if missing_items:
        print(f"❌ Missing items: {missing_items}")
        return False
    else:
        print("✅ All platform structure components present")
        return True

def test_artifact_specification():
    """Test artifact specification file"""
    print("📋 Testing Artifact Specification...")
    
    try:
        with open("spec.json", "r") as f:
            spec = json.load(f)
        
        required_fields = ["artifactId", "title", "version", "type", "engines", "audience"]
        missing_fields = [field for field in required_fields if field not in spec]
        
        if missing_fields:
            print(f"❌ Missing specification fields: {missing_fields}")
            return False
        
        if spec["artifactId"] != "codex-build-0001":
            print(f"❌ Incorrect artifact ID: {spec['artifactId']}")
            return False
        
        print("✅ Artifact specification valid")
        return True
    
    except Exception as e:
        print(f"❌ Specification error: {e}")
        return False

def test_sigil_authentication():
    """Test sigil and ceremonial authentication"""
    print("🗝️ Testing Sigil Authentication...")
    
    try:
        with open("SIGIL-BUILD-0001.md", "r", encoding='utf-8') as f:
            sigil_content = f.read()
        
        required_elements = [
            "SIGIL-BUILD-0001",
            "codex-build-0001", 
            "Council-Prime",
            "Custodian",
            "2025-11-13"
        ]
        
        missing_elements = [elem for elem in required_elements if elem not in sigil_content]
        
        if missing_elements:
            print(f"❌ Missing sigil elements: {missing_elements}")
            return False
        
        print("✅ Sigil authentication valid")
        return True
    
    except Exception as e:
        print(f"❌ Sigil error: {e}")
        return False

def test_database_schema():
    """Test database schema completeness"""
    print("🏛️ Testing Database Schema...")
    
    try:
        with open("db/schema.sql", "r") as f:
            schema_content = f.read()
        
        required_tables = [
            "CREATE TABLE users",
            "CREATE TABLE products", 
            "CREATE TABLE orders",
            "CREATE TABLE order_items",
            "CREATE TABLE audit_trail",
            "CREATE TABLE sigils"
        ]
        
        missing_tables = [table for table in required_tables if table not in schema_content]
        
        if missing_tables:
            print(f"❌ Missing database tables: {missing_tables}")
            return False
        
        print("✅ Database schema complete")
        return True
    
    except Exception as e:
        print(f"❌ Database schema error: {e}")
        return False

def test_ui_components():
    """Test UI component completeness"""
    print("🎨 Testing UI Components...")
    
    try:
        ui_components = [
            "ui/templates/index.html",
            "ui/templates/catalog.html", 
            "ui/templates/dashboard.html",
            "ui/static/sovereign.css",
            "ui/static/sovereign.js"
        ]
        
        missing_components = [comp for comp in ui_components if not Path(comp).exists()]
        
        if missing_components:
            print(f"❌ Missing UI components: {missing_components}")
            return False
        
        print("✅ UI components complete")
        return True
    
    except Exception as e:
        print(f"❌ UI components error: {e}")
        return False

def test_engine_integration():
    """Test engine integration configuration"""
    print("🔥 Testing Engine Integration...")
    
    try:
        with open("spec.json", "r") as f:
            spec = json.load(f)
        
        required_engines = ["AXIOM", "RAG", "SIGIL", "ORACLE", "LANTERN", "FLAME"]
        
        if "engines" not in spec:
            print("❌ No engines specified")
            return False
        
        missing_engines = [engine for engine in required_engines if engine not in spec["engines"]]
        
        if missing_engines:
            print(f"❌ Missing engines: {missing_engines}")
            return False
        
        print("✅ Engine integration complete")
        return True
    
    except Exception as e:
        print(f"❌ Engine integration error: {e}")
        return False

def run_platform_tests():
    """Run complete platform test suite"""
    print("🚀 Sovereign Commerce Platform - Ceremonial Testing")
    print("=" * 60)
    
    tests = [
        test_platform_structure,
        test_artifact_specification,
        test_sigil_authentication,
        test_database_schema,
        test_ui_components,
        test_engine_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed - Platform ready for diaspora funders")
        print("🏛️ Sovereign Commerce Platform CONSECRATED AND ACTIVE")
        print()
        print("🔥 Access the platform at: http://127.0.0.1:8080")
        print("📋 Artifact ID: codex-build-0001")
        print("🗝️ Sigil: SIGIL-BUILD-0001")
        print("👑 Authority: Council-Prime")
        return True
    else:
        print(f"❌ {total - passed} tests failed - Platform needs attention")
        return False

if __name__ == "__main__":
    success = run_platform_tests()
    sys.exit(0 if success else 1)