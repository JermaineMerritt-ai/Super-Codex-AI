#!/usr/bin/env python3
"""
System Restoration Verification Script
Verifies all critical files have been restored and are functional
"""

import sys
import os
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status"""
    path = Path(file_path)
    if path.exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MISSING")
        return False

def test_import(module_path, description):
    """Test if a module can be imported"""
    try:
        exec(f"import {module_path}")
        print(f"✅ {description}: {module_path}")
        return True
    except Exception as e:
        print(f"❌ {description}: {module_path} - ERROR: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Super-Codex-AI System Restoration Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Critical files check
    print("\n📁 Critical Files Check:")
    critical_files = [
        ("backend/app/gateway.py", "Service Gateway"),
        ("backend/app/auth.py", "Authentication Module"),
        ("backend/app/auth_routes.py", "Auth Routes"),
        ("backend/app/health.py", "Health Checks"),
        ("backend/api/webhooks.py", "Webhooks API"),
        ("backend/api/upload.py", "Upload API"),
        ("ceremonial_interface.py", "Ceremonial Interface"),
        ("service_monitor.py", "Service Monitor"),
        ("systemd_crown.py", "SystemD Crown"),
        ("requirements.txt", "Dependencies"),
        ("simple_server.py", "Main Server"),
        ("logs/", "Logs Directory")
    ]
    
    for file_path, description in critical_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Import tests
    print("\n🐍 Import Tests:")
    import_tests = [
        ("simple_server", "Main Server Module"),
        ("backend.app.health", "Health Module"),
        ("backend.app.gateway", "Gateway Module"),
        ("backend.app.auth", "Auth Module"),
        ("ceremonial_interface", "Ceremonial Interface"),
        ("service_monitor", "Service Monitor"),
        ("systemd_crown", "SystemD Crown")
    ]
    
    sys.path.insert(0, ".")
    for module_path, description in import_tests:
        if not test_import(module_path, description):
            all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✨ The Super-Codex-AI system has been fully restored!")
        print("\n🚀 You can now start the server with:")
        print("   python -m uvicorn simple_server:app --host 0.0.0.0 --port 8080")
        print("\n🔗 Available endpoints:")
        print("   http://localhost:8080/health/ - Health check")
        print("   http://localhost:8080/ceremonial/ - Ceremonial dashboard")
        print("   http://localhost:8080/woocommerce/ - WooCommerce interface")
        print("   http://localhost:8080/docs - API documentation")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please review the errors above and ensure all files are properly restored.")
        return 1

if __name__ == "__main__":
    exit(main())