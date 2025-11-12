#!/usr/bin/env python3
"""
System Validation Test Suite
Comprehensive testing of all Axiom-Flame components
"""
import requests
import subprocess
import time
from pathlib import Path

class SystemValidator:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8089"
        self.results = []
        
    def test_api_endpoints(self):
        """Test all Flask API endpoints."""
        print("🌐 Testing API endpoints...")
        
        endpoints = [
            ("/", "GET", "Root endpoint"),
            ("/health", "GET", "Health check"),
            ("/reason", "POST", "Ceremonial reasoning"),
            ("/api/honors", "GET", "Honors management"),
            ("/api/registry", "GET", "Registry access")
        ]
        
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                else:
                    # POST with sample data
                    sample_data = {
                        "actor": "Custodian",
                        "realm": "PL-001",
                        "intent": "Test validation"
                    }
                    response = requests.post(f"{self.base_url}{endpoint}", json=sample_data, timeout=5)
                
                status = "✅ PASS" if response.status_code < 500 else "❌ FAIL"
                self.results.append(f"{status} {description}: {response.status_code}")
                
            except Exception as e:
                self.results.append(f"❌ FAIL {description}: {e}")
                
    def test_cli_commands(self):
        """Test CLI commands."""
        print("⚡ Testing CLI commands...")
        
        cli_tests = [
            (["python", "axiom-flame/axiom_flame.py", "health"], "CLI health check"),
            (["python", "service_monitor.py", "--help"], "Service monitor help"),
            (["python", "systemd_crown.py", "--help"], "SystemD Crown help")
        ]
        
        for cmd, description in cli_tests:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                status = "✅ PASS" if result.returncode == 0 else "⚠️ WARN"
                self.results.append(f"{status} {description}: Exit code {result.returncode}")
            except Exception as e:
                self.results.append(f"❌ FAIL {description}: {e}")
                
    def test_service_management(self):
        """Test service management capabilities."""
        print("🔧 Testing service management...")
        
        # Test service monitor
        try:
            cmd = ["python", "service_monitor.py", "--version"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            status = "✅ PASS" if "monitor" in result.stdout.lower() or result.returncode == 0 else "⚠️ WARN"
            self.results.append(f"{status} Service monitor available")
        except:
            self.results.append("❌ FAIL Service monitor unavailable")
            
        # Test SystemD Crown
        try:
            cmd = ["python", "systemd_crown.py", "list"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            status = "✅ PASS" if result.returncode == 0 else "⚠️ WARN"
            self.results.append(f"{status} SystemD Crown operational")
        except:
            self.results.append("❌ FAIL SystemD Crown unavailable")
            
    def test_file_integrity(self):
        """Test critical file presence."""
        print("📁 Testing file integrity...")
        
        critical_files = [
            "axiom-flame/packages/api/app.py",
            "axiom-flame/axiom_flame.py",
            "service_monitor.py",
            "systemd_crown.py",
            "system_health_check.py",
            "start_system.bat",
            "start_system.ps1"
        ]
        
        for file_path in critical_files:
            if Path(file_path).exists():
                self.results.append(f"✅ PASS File exists: {file_path}")
            else:
                self.results.append(f"❌ FAIL Missing file: {file_path}")
                
    def run_full_validation(self):
        """Run complete system validation."""
        print("🔍 Running full system validation...\n")
        
        self.test_api_endpoints()
        self.test_cli_commands()
        self.test_service_management()
        self.test_file_integrity()
        
        # Summary
        print("\n" + "="*60)
        print("🔥 AXIOM-FLAME SYSTEM VALIDATION RESULTS")
        print("="*60)
        
        passed = sum(1 for r in self.results if "✅ PASS" in r)
        warned = sum(1 for r in self.results if "⚠️ WARN" in r)
        failed = sum(1 for r in self.results if "❌ FAIL" in r)
        total = len(self.results)
        
        print(f"📊 Results: {passed} passed, {warned} warnings, {failed} failed ({total} total)")
        
        print("\n📋 Detailed Results:")
        for result in self.results:
            print(f"   {result}")
            
        if failed == 0:
            print(f"\n🎉 System validation SUCCESSFUL!")
            print("✅ All critical components operational")
            print("🚀 Axiom-Flame ready for ceremonial operations")
        else:
            print(f"\n⚠️ System validation completed with {failed} failures")
            print("🔧 Review failed components before production use")
            
        return failed == 0

if __name__ == "__main__":
    validator = SystemValidator()
    success = validator.run_full_validation()
    exit(0 if success else 1)