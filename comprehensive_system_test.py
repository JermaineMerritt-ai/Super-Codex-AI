#!/usr/bin/env python3
"""
Comprehensive system test and issue fixer
Tests all endpoints, templates, and functionality
"""
import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:8004"
RESULTS = {
    "working_endpoints": [],
    "broken_endpoints": [],
    "missing_files": [],
    "errors": [],
    "fixes_applied": []
}

def test_endpoint(endpoint, description):
    """Test a single endpoint"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            RESULTS["working_endpoints"].append({
                "endpoint": endpoint,
                "description": description,
                "status": response.status_code
            })
            print(f"✅ {endpoint} - {description}")
            return True
        else:
            RESULTS["broken_endpoints"].append({
                "endpoint": endpoint,
                "description": description,
                "status": response.status_code,
                "error": response.text
            })
            print(f"❌ {endpoint} - {description} (Status: {response.status_code})")
            return False
    except Exception as e:
        RESULTS["broken_endpoints"].append({
            "endpoint": endpoint,
            "description": description,
            "error": str(e)
        })
        print(f"❌ {endpoint} - {description} (Error: {e})")
        return False

def test_all_endpoints():
    """Test all known endpoints"""
    print("🧪 Testing All Endpoints...")
    print("=" * 50)
    
    # Core endpoints
    test_endpoint("/", "Root endpoint")
    test_endpoint("/health", "Health check")
    test_endpoint("/ready", "Readiness check")
    test_endpoint("/api/status", "API status")
    
    # Dominion endpoints
    test_endpoint("/dominion", "Main dominion interface")
    test_endpoint("/dominion/roles", "Role selector")
    test_endpoint("/dominion/engines", "Six-Engine interface")
    test_endpoint("/dominion/ceremony", "Ceremonial dashboard")
    test_endpoint("/dominion/command", "Command center")
    
    # Role-specific endpoints
    test_endpoint("/dominion/role/contributor", "Contributor role")
    test_endpoint("/dominion/role/council", "Council role")
    test_endpoint("/dominion/role/heir", "Heir role")
    test_endpoint("/dominion/role/general", "General role")
    
    # Scroll endpoints
    test_endpoint("/dominion/scroll/welcome", "Welcome scroll")
    test_endpoint("/dominion/scroll/custodian_principles", "Custodian principles")
    
    # Status endpoints
    test_endpoint("/dominion/axiom/status", "Axiom flame status")
    
    print("\\n" + "=" * 50)

def test_role_scroll_apis():
    """Test role-specific scroll APIs"""
    print("📜 Testing Role Scroll APIs...")
    print("=" * 50)
    
    roles = ["contributor", "council", "heir", "general"]
    for role in roles:
        try:
            response = requests.get(f"{BASE_URL}/dominion/role/{role}/scrolls", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {role} scrolls API - {len(data.get('recent_scrolls', []))} scrolls")
                RESULTS["working_endpoints"].append({
                    "endpoint": f"/dominion/role/{role}/scrolls",
                    "description": f"{role} scrolls API",
                    "status": response.status_code
                })
            else:
                print(f"❌ {role} scrolls API (Status: {response.status_code})")
                RESULTS["broken_endpoints"].append({
                    "endpoint": f"/dominion/role/{role}/scrolls",
                    "description": f"{role} scrolls API",
                    "status": response.status_code
                })
        except Exception as e:
            print(f"❌ {role} scrolls API (Error: {e})")
            RESULTS["errors"].append(f"Role {role} scrolls API error: {e}")
    
    print("\\n" + "=" * 50)

def check_template_files():
    """Check if all template files exist"""
    print("📄 Checking Template Files...")
    print("=" * 50)
    
    templates_dir = Path("templates")
    expected_templates = [
        "ceremonial_dominion.html",
        "role_selector.html", 
        "role_dominion.html",
        "six_engine_dominion.html",
        "command_center.html",
        "dominion_index.html"
    ]
    
    for template in expected_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - MISSING")
            RESULTS["missing_files"].append(str(template_path))
    
    print("\\n" + "=" * 50)

def check_static_files():
    """Check if all static files exist"""
    print("🎨 Checking Static Files...")
    print("=" * 50)
    
    static_dir = Path("static")
    expected_static = [
        "ceremonial.css",
        "flame-simulation.js"
    ]
    
    for static_file in expected_static:
        static_path = static_dir / static_file
        if static_path.exists():
            print(f"✅ {static_file}")
        else:
            print(f"❌ {static_file} - MISSING")
            RESULTS["missing_files"].append(str(static_path))
    
    print("\\n" + "=" * 50)

def generate_report():
    """Generate comprehensive test report"""
    print("📊 COMPREHENSIVE SYSTEM REPORT")
    print("=" * 60)
    
    total_endpoints = len(RESULTS["working_endpoints"]) + len(RESULTS["broken_endpoints"])
    working_count = len(RESULTS["working_endpoints"])
    broken_count = len(RESULTS["broken_endpoints"])
    
    print(f"📈 ENDPOINT STATUS:")
    print(f"   ✅ Working: {working_count}")
    print(f"   ❌ Broken: {broken_count}")
    print(f"   📊 Total: {total_endpoints}")
    print(f"   💯 Success Rate: {(working_count/total_endpoints*100):.1f}%" if total_endpoints > 0 else "   💯 Success Rate: 0%")
    
    print(f"\\n📂 FILE STATUS:")
    print(f"   ❌ Missing Files: {len(RESULTS['missing_files'])}")
    print(f"   🐛 Errors Found: {len(RESULTS['errors'])}")
    
    if RESULTS["broken_endpoints"]:
        print(f"\\n💥 BROKEN ENDPOINTS:")
        for endpoint in RESULTS["broken_endpoints"]:
            print(f"   ❌ {endpoint['endpoint']} - {endpoint.get('error', 'Unknown error')}")
    
    if RESULTS["missing_files"]:
        print(f"\\n📁 MISSING FILES:")
        for file_path in RESULTS["missing_files"]:
            print(f"   ❌ {file_path}")
    
    if RESULTS["errors"]:
        print(f"\\n🐛 ERRORS:")
        for error in RESULTS["errors"]:
            print(f"   ❌ {error}")
    
    print(f"\\n🎯 SYSTEM STATUS:")
    if broken_count == 0 and len(RESULTS["missing_files"]) == 0 and len(RESULTS["errors"]) == 0:
        print("   🎉 SYSTEM FULLY OPERATIONAL!")
        print("   🔥 All endpoints working")
        print("   📄 All templates found") 
        print("   🎨 All static files found")
        print("   ✨ Zero errors detected")
    else:
        print("   ⚠️  Issues detected - fixes needed")
        
    print("\\n" + "=" * 60)
    
    # Save detailed report
    with open("comprehensive_test_report.json", "w") as f:
        json.dump(RESULTS, f, indent=2)
    
    print("📄 Detailed report saved to: comprehensive_test_report.json")

def main():
    """Run comprehensive system test"""
    print("🚀 SUPER-CODEX-AI COMPREHENSIVE SYSTEM TEST")
    print("🧑‍🚀 Who Is This For? - System Validation")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run all tests
    test_all_endpoints()
    test_role_scroll_apis()
    check_template_files()
    check_static_files()
    
    # Generate final report
    generate_report()
    
    print("\\n🎯 NEXT STEPS:")
    print("   1. Review comprehensive_test_report.json for details")
    print("   2. Access working system at: http://127.0.0.1:8003/dominion")
    print("   3. Try role selector at: http://127.0.0.1:8003/dominion/roles")
    print("   4. Use Six-Engine interface: http://127.0.0.1:8003/dominion/engines")

if __name__ == "__main__":
    main()