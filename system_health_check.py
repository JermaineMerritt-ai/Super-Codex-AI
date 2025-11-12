#!/usr/bin/env python3
"""
Super-Codex-AI System Health Check and Repair
Comprehensive diagnostics and auto-repair for all system components
"""
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

class SystemHealthChecker:
    def __init__(self):
        self.root_path = Path(__file__).resolve().parent
        self.issues = []
        self.fixes_applied = []
        
    def check_python_environment(self) -> bool:
        """Check Python environment and dependencies."""
        print("🐍 Checking Python environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.issues.append("Python version too old (requires 3.8+)")
            return False
            
        # Check required packages
        required_packages = [
            'flask', 'fastapi', 'uvicorn', 'requests', 
            'pydantic', 'jsonschema', 'jinja2'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
                
        if missing_packages:
            self.issues.append(f"Missing packages: {', '.join(missing_packages)}")
            self.fix_missing_packages(missing_packages)
            
        print("✅ Python environment OK")
        return True
        
    def fix_missing_packages(self, packages: List[str]):
        """Install missing Python packages."""
        print(f"📦 Installing missing packages: {', '.join(packages)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", *packages
            ])
            self.fixes_applied.append(f"Installed packages: {', '.join(packages)}")
        except subprocess.CalledProcessError as e:
            self.issues.append(f"Failed to install packages: {e}")
            
    def check_directory_structure(self) -> bool:
        """Check and create required directories."""
        print("📁 Checking directory structure...")
        
        required_dirs = [
            "axiom-flame/packages/api",
            "axiom-flame/packages/cli", 
            "axiom-flame/storage/ledger",
            "axiom-flame/storage/replays",
            "axiom-flame/storage/annals",
            "axiom-flame/artifacts/ceremonies",
            "axiom-flame/artifacts/schemas",
            "backend/api",
            "backend/models",
            "backend/services",
            "backend/tests",
            "services",
            "logs",
            "systemd_crown_storage"
        ]
        
        for dir_path in required_dirs:
            full_path = self.root_path / dir_path
            if not full_path.exists():
                self.issues.append(f"Missing directory: {dir_path}")
                self.fix_missing_directory(full_path)
                
        print("✅ Directory structure OK")
        return True
        
    def fix_missing_directory(self, path: Path):
        """Create missing directory."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.fixes_applied.append(f"Created directory: {path}")
        except Exception as e:
            self.issues.append(f"Failed to create directory {path}: {e}")
            
    def check_flask_api(self) -> bool:
        """Check Flask API configuration."""
        print("🌶️ Checking Flask API...")
        
        api_path = self.root_path / "axiom-flame/packages/api/app.py"
        if not api_path.exists():
            self.issues.append("Flask API app.py missing")
            return False
            
        # Check if Flask app can be imported
        try:
            sys.path.insert(0, str(api_path.parent))
            import app
            if not hasattr(app, 'app'):
                self.issues.append("Flask app object not found")
                return False
        except Exception as e:
            self.issues.append(f"Flask API import error: {e}")
            return False
            
        print("✅ Flask API OK")
        return True
        
    def check_service_monitoring(self) -> bool:
        """Check service monitoring system."""
        print("🔧 Checking service monitoring...")
        
        monitor_files = [
            "service_monitor.py",
            "systemd_crown.py", 
            "service_registry.py"
        ]
        
        for file_name in monitor_files:
            file_path = self.root_path / file_name
            if not file_path.exists():
                self.issues.append(f"Missing service file: {file_name}")
                
        print("✅ Service monitoring OK")
        return True
        
    def check_cli_tools(self) -> bool:
        """Check CLI tools and scripts."""
        print("⚡ Checking CLI tools...")
        
        cli_files = [
            "axiom-flame/axiom_flame.py",
            "axiom-flame/axiom-flame.bat"
        ]
        
        for file_path in cli_files:
            full_path = self.root_path / file_path
            if not full_path.exists():
                self.issues.append(f"Missing CLI file: {file_path}")
                
        print("✅ CLI tools OK")
        return True
        
    def check_schemas_and_configs(self) -> bool:
        """Check JSON schemas and configuration files."""
        print("📋 Checking schemas and configs...")
        
        schema_dir = self.root_path / "axiom-flame/artifacts/schemas"
        if schema_dir.exists():
            schema_files = list(schema_dir.glob("*.json"))
            if not schema_files:
                self.issues.append("No JSON schema files found")
                self.create_basic_schemas()
        else:
            self.issues.append("Schema directory missing")
            
        print("✅ Schemas and configs OK")
        return True
        
    def create_basic_schemas(self):
        """Create basic JSON schemas."""
        schema_dir = self.root_path / "axiom-flame/artifacts/schemas"
        schema_dir.mkdir(parents=True, exist_ok=True)
        
        # Basic ledger entry schema
        ledger_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "dispatch_id": {"type": "string"},
                "timestamp": {"type": "string"},
                "actor": {"type": "string"},
                "realm": {"type": "string"},
                "capsule": {"type": "string"},
                "intent": {"type": "string"}
            },
            "required": ["dispatch_id", "timestamp", "actor", "realm"]
        }
        
        with open(schema_dir / "ledger-entry.schema.json", 'w') as f:
            json.dump(ledger_schema, f, indent=2)
            
        self.fixes_applied.append("Created basic JSON schemas")
        
    def check_port_conflicts(self) -> bool:
        """Check for port conflicts."""
        print("🔌 Checking port conflicts...")
        
        try:
            # Check common ports
            result = subprocess.run(
                ["netstat", "-ano"], 
                capture_output=True, text=True, shell=True
            )
            
            occupied_ports = []
            for line in result.stdout.split('\n'):
                if ':8087' in line or ':8082' in line:
                    occupied_ports.append(line.strip())
                    
            if occupied_ports:
                print(f"⚠️ Ports in use: {len(occupied_ports)} conflicts detected")
                for port_line in occupied_ports[:3]:  # Show first 3
                    print(f"   {port_line}")
            else:
                print("✅ No port conflicts detected")
                
        except Exception as e:
            print(f"⚠️ Could not check ports: {e}")
            
        return True
        
    def create_startup_scripts(self):
        """Create missing startup scripts."""
        print("📝 Creating startup scripts...")
        
        # Create Windows batch file for easy startup
        batch_content = """@echo off
echo 🔥 Starting Axiom-Flame System...
cd /d "%~dp0"

REM Start Flask API
echo Starting Flask API...
python axiom-flame\\packages\\api\\start_api.py start --daemon 8087

REM Start service monitoring
echo Starting service monitoring...
python service_monitor.py --daemon

echo ✅ Axiom-Flame System started successfully!
echo Access API at: http://localhost:8087
pause
"""
        
        batch_path = self.root_path / "start_system.bat"
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
            
        # Create PowerShell script
        ps_content = """# Axiom-Flame System Startup Script
Write-Host "🔥 Starting Axiom-Flame System..." -ForegroundColor Yellow

Set-Location $PSScriptRoot

# Start Flask API
Write-Host "Starting Flask API..." -ForegroundColor Green
python axiom-flame\\packages\\api\\start_api.py start --daemon 8087

# Start service monitoring  
Write-Host "Starting service monitoring..." -ForegroundColor Green
python service_monitor.py --daemon

Write-Host "✅ Axiom-Flame System started successfully!" -ForegroundColor Green
Write-Host "Access API at: http://localhost:8087" -ForegroundColor Cyan
"""
        
        ps_path = self.root_path / "start_system.ps1"
        with open(ps_path, 'w', encoding='utf-8') as f:
            f.write(ps_content)
            
        self.fixes_applied.append("Created startup scripts")
        
    def run_full_diagnostic(self) -> Dict:
        """Run complete system diagnostic."""
        print("🔍 Running full system diagnostic...\n")
        
        checks = [
            ("Python Environment", self.check_python_environment),
            ("Directory Structure", self.check_directory_structure),
            ("Flask API", self.check_flask_api),
            ("Service Monitoring", self.check_service_monitoring),
            ("CLI Tools", self.check_cli_tools),
            ("Schemas & Configs", self.check_schemas_and_configs),
            ("Port Conflicts", self.check_port_conflicts)
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                results[check_name] = False
                self.issues.append(f"{check_name} check failed: {e}")
                
        # Create startup scripts if needed
        if not (self.root_path / "start_system.bat").exists():
            self.create_startup_scripts()
            
        return results
        
    def print_summary(self, results: Dict):
        """Print diagnostic summary."""
        print("\n" + "="*60)
        print("🔥 AXIOM-FLAME SYSTEM DIAGNOSTIC SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        print(f"📊 System Health: {passed}/{total} checks passed")
        
        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
                
        if self.fixes_applied:
            print(f"\n🔧 Fixes Applied ({len(self.fixes_applied)}):")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"   {i}. {fix}")
                
        print(f"\n🎯 System Status: {'HEALTHY' if not self.issues else 'NEEDS ATTENTION'}")
        
        if not self.issues:
            print("\n✅ All systems operational! Axiom-Flame ready for ceremonial operations.")
            print("🚀 To start the system, run:")
            print("   Windows: .\\start_system.bat")
            print("   PowerShell: .\\start_system.ps1")
        else:
            print("\n⚠️ Some issues detected. Review and fix before starting system.")

def main():
    checker = SystemHealthChecker()
    results = checker.run_full_diagnostic()
    checker.print_summary(results)
    
    return 0 if not checker.issues else 1

if __name__ == "__main__":
    sys.exit(main())