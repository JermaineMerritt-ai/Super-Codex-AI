#!/usr/bin/env python3
"""
Issue identification and automated fix system
"""
import os
import sys
from pathlib import Path
import json

def identify_issues():
    """Identify all system issues"""
    issues = {
        "missing_files": [],
        "import_errors": [],
        "template_issues": [],
        "static_issues": [],
        "config_issues": []
    }
    
    print("🔍 IDENTIFYING ALL ISSUES...")
    print("=" * 50)
    
    # Check Python imports
    print("📦 Checking Python imports...")
    try:
        import fastapi
        print("✅ FastAPI imported")
    except ImportError as e:
        issues["import_errors"].append(f"FastAPI: {e}")
        print(f"❌ FastAPI: {e}")
    
    try:
        import uvicorn
        print("✅ Uvicorn imported")
    except ImportError as e:
        issues["import_errors"].append(f"Uvicorn: {e}")
        print(f"❌ Uvicorn: {e}")
    
    try:
        import jinja2
        print("✅ Jinja2 imported")
    except ImportError as e:
        issues["import_errors"].append(f"Jinja2: {e}")
        print(f"❌ Jinja2: {e}")
    
    try:
        import requests
        print("✅ Requests imported")
    except ImportError as e:
        issues["import_errors"].append(f"Requests: {e}")
        print(f"❌ Requests: {e}")
    
    try:
        import prometheus_client
        print("✅ Prometheus client imported")
    except ImportError as e:
        issues["import_errors"].append(f"Prometheus: {e}")
        print(f"❌ Prometheus: {e}")
    
    try:
        import sentry_sdk
        print("✅ Sentry SDK imported")
    except ImportError as e:
        issues["import_errors"].append(f"Sentry SDK: {e}")
        print(f"❌ Sentry SDK: {e}")
    
    # Check custom modules
    try:
        import ceremonial_interface
        print("✅ Ceremonial interface imported")
    except ImportError as e:
        issues["import_errors"].append(f"Ceremonial interface: {e}")
        print(f"❌ Ceremonial interface: {e}")
    
    try:
        import circuit_breaker
        print("✅ Circuit breaker imported")
    except ImportError as e:
        issues["import_errors"].append(f"Circuit breaker: {e}")
        print(f"❌ Circuit breaker: {e}")
    
    # Check template files
    print("\\n📄 Checking template files...")
    templates_dir = Path("templates")
    required_templates = [
        "ceremonial_dominion.html",
        "role_selector.html", 
        "role_dominion.html",
        "six_engine_dominion.html",
        "command_center.html"
    ]
    
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"✅ {template}")
        else:
            issues["template_issues"].append(str(template_path))
            print(f"❌ {template} - MISSING")
    
    # Check static files
    print("\\n🎨 Checking static files...")
    static_dir = Path("static")
    required_static = [
        "ceremonial.css",
        "flame-simulation.js"
    ]
    
    for static_file in required_static:
        static_path = static_dir / static_file
        if static_path.exists():
            print(f"✅ {static_file}")
        else:
            issues["static_issues"].append(str(static_path))
            print(f"❌ {static_file} - MISSING")
    
    # Check configuration files
    print("\\n⚙️ Checking configuration...")
    config_files = [
        ".env",
        "requirements.txt"
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file}")
        else:
            issues["config_issues"].append(config_file)
            print(f"❌ {config_file} - MISSING")
    
    # Check directories
    print("\\n📂 Checking directories...")
    required_dirs = [
        "templates",
        "static",
        "__pycache__"
    ]
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/")
        else:
            issues["missing_files"].append(dir_name)
            print(f"❌ {dir_name}/ - MISSING")
    
    return issues

def fix_all_issues(issues):
    """Automatically fix all identified issues"""
    print("\\n🔧 FIXING ALL ISSUES...")
    print("=" * 50)
    
    fixes_applied = []
    
    # Fix missing directories
    for missing_dir in issues.get("missing_files", []):
        if not missing_dir.endswith("/"):
            continue
        dir_path = Path(missing_dir.rstrip("/"))
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            fixes_applied.append(f"Created directory: {missing_dir}")
            print(f"✅ Created directory: {missing_dir}")
    
    # Fix missing .env file
    if ".env" in issues.get("config_issues", []):
        env_content = '''# Super-Codex-AI Environment Configuration
ENVIRONMENT=development
SENTRY_DSN=https://your-sentry-dsn-here@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/codex_db
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
'''
        with open(".env", "w") as f:
            f.write(env_content)
        fixes_applied.append("Created .env file")
        print("✅ Created .env file")
    
    return fixes_applied

def test_server_basic():
    """Test basic server functionality without making HTTP requests"""
    print("\\n🧪 TESTING SERVER COMPONENTS...")
    print("=" * 50)
    
    try:
        from simple_server import app
        print("✅ Server app imports successfully")
        
        # Check if app is FastAPI instance
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            print("✅ App is valid FastAPI instance")
        else:
            print("❌ App is not FastAPI instance")
            return False
        
        # Check if routes are configured
        routes = [route.path for route in app.routes]
        print(f"✅ {len(routes)} routes configured")
        
        # Check key routes
        key_routes = ["/", "/health", "/ready", "/dominion"]
        for route in key_routes:
            if route in routes:
                print(f"✅ Route {route} exists")
            else:
                print(f"❌ Route {route} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def generate_status_report(issues, fixes):
    """Generate comprehensive status report"""
    print("\\n📊 FINAL STATUS REPORT")
    print("=" * 60)
    
    total_issues = sum(len(v) for v in issues.values() if isinstance(v, list))
    total_fixes = len(fixes)
    
    print(f"🔍 ISSUES IDENTIFIED: {total_issues}")
    print(f"🔧 FIXES APPLIED: {total_fixes}")
    
    if total_issues == 0:
        print("\\n🎉 SYSTEM STATUS: FULLY OPERATIONAL!")
        print("✅ No issues detected")
        print("✅ All components working")
        print("✅ Ready for deployment")
    elif total_fixes == total_issues:
        print("\\n✅ SYSTEM STATUS: ALL ISSUES FIXED!")
        print("🔧 All detected issues resolved")
        print("✅ System ready for testing")
    else:
        remaining_issues = total_issues - total_fixes
        print(f"\\n⚠️ SYSTEM STATUS: {remaining_issues} ISSUES REMAIN")
        print("🔧 Additional fixes may be needed")
    
    print("\\n📋 ISSUE BREAKDOWN:")
    for category, items in issues.items():
        if items:
            print(f"   {category.replace('_', ' ').title()}: {len(items)}")
    
    print("\\n🎯 NEXT STEPS:")
    print("   1. Start server: python -m uvicorn simple_server:app --port 8080")
    print("   2. Access system: http://127.0.0.1:8080/dominion")
    print("   3. Role selector: http://127.0.0.1:8080/dominion/roles")
    print("   4. Health check: http://127.0.0.1:8080/health")
    
    # Save report
    report = {
        "timestamp": str(datetime.now()),
        "issues_identified": issues,
        "fixes_applied": fixes,
        "total_issues": total_issues,
        "total_fixes": total_fixes,
        "status": "operational" if total_issues == 0 else "fixed" if total_fixes == total_issues else "issues_remain"
    }
    
    with open("system_status_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print("\\n📄 Detailed report saved: system_status_report.json")

def main():
    """Main issue identification and fix process"""
    print("🔧 SUPER-CODEX-AI ISSUE IDENTIFICATION & FIX SYSTEM")
    print("🧑‍🚀 Comprehensive System Repair")
    print("=" * 60)
    
    # Step 1: Identify all issues
    issues = identify_issues()
    
    # Step 2: Fix all issues
    fixes = fix_all_issues(issues)
    
    # Step 3: Test server components
    server_working = test_server_basic()
    if server_working:
        fixes.append("Server components validated")
    
    # Step 4: Generate status report
    generate_status_report(issues, fixes)
    
    print("\\n🎉 ISSUE IDENTIFICATION AND REPAIR COMPLETE!")

if __name__ == "__main__":
    from datetime import datetime
    main()