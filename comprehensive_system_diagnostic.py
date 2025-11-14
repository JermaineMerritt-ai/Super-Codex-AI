#!/usr/bin/env python3
"""
Comprehensive System Diagnostic Tool
Identifies all problems, issues, and errors in the Super-Codex-AI system
"""
import os
import sys
import json
import subprocess
import importlib
import traceback
from pathlib import Path
from datetime import datetime
import ast
import platform

class SystemDiagnostic:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.info = []
        self.critical_errors = []
        self.python_issues = []
        self.file_issues = []
        self.dependency_issues = []
        
    def log_issue(self, category, level, message, details=None):
        """Log an issue with categorization"""
        issue = {
            "category": category,
            "level": level,  # "critical", "error", "warning", "info"
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        
        if level == "critical":
            self.critical_errors.append(issue)
        elif level == "error":
            self.issues.append(issue)
        elif level == "warning":
            self.warnings.append(issue)
        else:
            self.info.append(issue)
        
        # Categorize by type
        if category.startswith("python"):
            self.python_issues.append(issue)
        elif category.startswith("file"):
            self.file_issues.append(issue)
        elif category.startswith("dependency"):
            self.dependency_issues.append(issue)
    
    def check_python_environment(self):
        """Check Python environment and version"""
        print("🐍 Checking Python Environment...")
        
        # Python version check
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            self.log_issue("python_version", "error", 
                         f"Python version {python_version.major}.{python_version.minor} is outdated. Recommend 3.8+")
        else:
            self.log_issue("python_version", "info", 
                         f"Python version {python_version.major}.{python_version.minor}.{python_version.micro} is acceptable")
        
        # Virtual environment check
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.log_issue("python_venv", "info", "Virtual environment is active")
        else:
            self.log_issue("python_venv", "warning", "No virtual environment detected")
        
        # Check Python path
        python_path = sys.executable
        self.log_issue("python_path", "info", f"Python executable: {python_path}")
        
        # Check installed packages
        try:
            result = subprocess.run([python_path, "-m", "pip", "list"], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                packages = result.stdout.strip().split('\n')
                self.log_issue("python_packages", "info", 
                             f"Found {len(packages)-2} installed packages")  # -2 for header lines
            else:
                self.log_issue("python_packages", "error", "Failed to list installed packages")
        except Exception as e:
            self.log_issue("python_packages", "error", f"Error checking packages: {e}")
    
    def check_required_dependencies(self):
        """Check required Python dependencies"""
        print("📦 Checking Dependencies...")
        
        required_packages = [
            'fastapi', 'uvicorn', 'jinja2', 'requests', 'pydantic',
            'python-multipart', 'aiofiles', 'python-dotenv'
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.log_issue("dependency_check", "info", f"✅ {package} is available")
            except ImportError as e:
                self.log_issue("dependency_check", "error", 
                             f"❌ {package} is missing", {"import_error": str(e)})
    
    def check_file_structure(self):
        """Check critical file structure"""
        print("📁 Checking File Structure...")
        
        critical_files = {
            "simple_server.py": "Main server file",
            "ceremonial_interface.py": "Ceremonial interface module",
            "circuit_breaker.py": "Circuit breaker utility",
            ".env": "Environment variables file"
        }
        
        critical_directories = {
            "templates": "Template files directory",
            "static": "Static files directory"
        }
        
        template_files = {
            "templates/ceremonial_dominion.html": "Main ceremonial interface",
            "templates/role_selector.html": "Role selector interface",
            "templates/role_dominion.html": "Role-specific interfaces",
            "templates/six_engine_dominion.html": "Six-engine interface",
            "templates/command_center.html": "Command center interface"
        }
        
        static_files = {
            "static/ceremonial.css": "Main stylesheet",
            "static/flame-simulation.js": "Flame simulation script"
        }
        
        # Check critical files
        for file_path, description in critical_files.items():
            if Path(file_path).exists():
                self.log_issue("file_structure", "info", f"✅ {description}: {file_path}")
            else:
                self.log_issue("file_structure", "error", f"❌ Missing {description}: {file_path}")
        
        # Check directories
        for dir_path, description in critical_directories.items():
            if Path(dir_path).exists() and Path(dir_path).is_dir():
                self.log_issue("file_structure", "info", f"✅ {description}: {dir_path}")
            else:
                self.log_issue("file_structure", "error", f"❌ Missing {description}: {dir_path}")
        
        # Check template files
        for file_path, description in template_files.items():
            if Path(file_path).exists():
                self.log_issue("file_structure", "info", f"✅ {description}: {file_path}")
            else:
                self.log_issue("file_structure", "error", f"❌ Missing {description}: {file_path}")
        
        # Check static files
        for file_path, description in static_files.items():
            if Path(file_path).exists():
                self.log_issue("file_structure", "info", f"✅ {description}: {file_path}")
            else:
                self.log_issue("file_structure", "error", f"❌ Missing {description}: {file_path}")
    
    def check_python_syntax(self):
        """Check Python files for syntax errors"""
        print("🔍 Checking Python Syntax...")
        
        python_files = [
            "simple_server.py",
            "ceremonial_interface.py", 
            "circuit_breaker.py"
        ]
        
        for file_path in python_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse the file for syntax errors
                    ast.parse(content, filename=file_path)
                    self.log_issue("python_syntax", "info", f"✅ {file_path} syntax is valid")
                    
                except SyntaxError as e:
                    self.log_issue("python_syntax", "error", 
                                 f"❌ Syntax error in {file_path}", 
                                 {"line": e.lineno, "error": str(e)})
                except Exception as e:
                    self.log_issue("python_syntax", "warning", 
                                 f"⚠️ Could not parse {file_path}: {e}")
    
    def check_imports(self):
        """Check if all imports work correctly"""
        print("📥 Checking Imports...")
        
        test_imports = [
            ("simple_server", "Main server module"),
            ("ceremonial_interface", "Ceremonial interface module"),
            ("circuit_breaker", "Circuit breaker module")
        ]
        
        for module_name, description in test_imports:
            try:
                importlib.import_module(module_name)
                self.log_issue("python_imports", "info", f"✅ {description} imports successfully")
            except ImportError as e:
                self.log_issue("python_imports", "error", 
                             f"❌ {description} import failed", {"error": str(e)})
            except Exception as e:
                self.log_issue("python_imports", "error", 
                             f"❌ {description} import error", {"error": str(e)})
    
    def check_server_configuration(self):
        """Check server configuration"""
        print("⚙️ Checking Server Configuration...")
        
        # Check if we can create a FastAPI app instance
        try:
            from simple_server import app
            self.log_issue("server_config", "info", "✅ FastAPI app instance created successfully")
            
            # Check available routes
            routes = [route.path for route in app.routes if hasattr(route, 'path')]
            self.log_issue("server_config", "info", f"✅ Found {len(routes)} configured routes")
            
            # Check for critical routes
            critical_routes = ["/", "/health", "/dominion", "/dominion/roles"]
            for route in critical_routes:
                if route in routes:
                    self.log_issue("server_config", "info", f"✅ Critical route available: {route}")
                else:
                    self.log_issue("server_config", "error", f"❌ Missing critical route: {route}")
                    
        except Exception as e:
            self.log_issue("server_config", "critical", 
                         f"❌ Cannot create FastAPI app", {"error": str(e)})
    
    def check_environment_variables(self):
        """Check environment variables"""
        print("🌍 Checking Environment Variables...")
        
        # Check if .env file exists
        env_file = Path(".env")
        if env_file.exists():
            self.log_issue("env_vars", "info", "✅ .env file exists")
            
            try:
                with open(".env", "r") as f:
                    env_content = f.read()
                    
                # Look for common variables
                common_vars = ["DEBUG", "HOST", "PORT", "ENVIRONMENT"]
                for var in common_vars:
                    if var in env_content:
                        self.log_issue("env_vars", "info", f"✅ {var} variable defined")
                    else:
                        self.log_issue("env_vars", "warning", f"⚠️ {var} variable not found")
                        
            except Exception as e:
                self.log_issue("env_vars", "error", f"❌ Cannot read .env file: {e}")
        else:
            self.log_issue("env_vars", "warning", "⚠️ .env file not found")
    
    def check_system_resources(self):
        """Check system resources and requirements"""
        print("💻 Checking System Resources...")
        
        # Platform info
        system_info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version()
        }
        
        self.log_issue("system_info", "info", "System Information", system_info)
        
        # Check available disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(Path.cwd())
            gb_free = free // (1024**3)
            
            if gb_free < 1:
                self.log_issue("system_resources", "error", 
                             f"❌ Low disk space: {gb_free}GB free")
            elif gb_free < 5:
                self.log_issue("system_resources", "warning", 
                             f"⚠️ Limited disk space: {gb_free}GB free")
            else:
                self.log_issue("system_resources", "info", 
                             f"✅ Adequate disk space: {gb_free}GB free")
                
        except Exception as e:
            self.log_issue("system_resources", "warning", 
                         f"⚠️ Could not check disk space: {e}")
    
    def check_port_availability(self):
        """Check if required ports are available"""
        print("🔌 Checking Port Availability...")
        
        import socket
        
        test_ports = [8000, 8001, 8002, 8003, 8004, 8080]
        
        for port in test_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.log_issue("port_check", "info", f"✅ Port {port} is available")
            except OSError:
                self.log_issue("port_check", "warning", f"⚠️ Port {port} is in use")
    
    def run_full_diagnostic(self):
        """Run complete system diagnostic"""
        print("=" * 70)
        print("🔧 SUPER-CODEX-AI COMPREHENSIVE SYSTEM DIAGNOSTIC")
        print("=" * 70)
        
        try:
            # Run all checks
            self.check_python_environment()
            self.check_required_dependencies()
            self.check_file_structure()
            self.check_python_syntax()
            self.check_imports()
            self.check_server_configuration()
            self.check_environment_variables()
            self.check_system_resources()
            self.check_port_availability()
            
            # Generate summary report
            self.generate_summary_report()
            
        except Exception as e:
            self.log_issue("diagnostic_system", "critical", 
                         f"Diagnostic system failed: {e}", 
                         {"traceback": traceback.format_exc()})
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 70)
        print("📊 DIAGNOSTIC SUMMARY REPORT")
        print("=" * 70)
        
        # Count issues by level
        critical_count = len(self.critical_errors)
        error_count = len(self.issues)
        warning_count = len(self.warnings)
        info_count = len(self.info)
        
        print(f"\n📈 ISSUE SUMMARY:")
        print(f"   🔴 Critical Errors: {critical_count}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   ⚠️ Warnings: {warning_count}")
        print(f"   ℹ️ Info: {info_count}")
        
        # Detailed breakdown
        if critical_count > 0:
            print(f"\n🔴 CRITICAL ERRORS ({critical_count}):")
            for issue in self.critical_errors:
                print(f"   • {issue['message']}")
                if issue['details']:
                    print(f"     Details: {issue['details']}")
        
        if error_count > 0:
            print(f"\n❌ ERRORS ({error_count}):")
            for issue in self.issues:
                print(f"   • {issue['message']}")
        
        if warning_count > 0:
            print(f"\n⚠️ WARNINGS ({warning_count}):")
            for issue in self.warnings:
                print(f"   • {issue['message']}")
        
        # Category breakdown
        print(f"\n📂 ISSUES BY CATEGORY:")
        print(f"   🐍 Python Issues: {len(self.python_issues)}")
        print(f"   📁 File Issues: {len(self.file_issues)}")
        print(f"   📦 Dependency Issues: {len(self.dependency_issues)}")
        
        # System status
        print(f"\n🎯 SYSTEM STATUS:")
        if critical_count > 0:
            print("   🔴 SYSTEM HAS CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED")
        elif error_count > 5:
            print("   ❌ SYSTEM HAS MULTIPLE ERRORS - ACTION REQUIRED")
        elif error_count > 0:
            print("   ⚠️ SYSTEM HAS SOME ERRORS - REVIEW RECOMMENDED")
        else:
            print("   ✅ SYSTEM IS OPERATIONAL")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if critical_count > 0:
            print("   1. Address all critical errors immediately")
            print("   2. Review server configuration")
            print("   3. Check Python imports and dependencies")
        
        if len(self.dependency_issues) > 0:
            print("   4. Install missing dependencies: pip install <package>")
        
        if len(self.file_issues) > 0:
            print("   5. Restore missing files from backup or recreate")
        
        if error_count == 0 and warning_count == 0:
            print("   ✅ System is healthy - no action required")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "critical_errors": critical_count,
                "errors": error_count,
                "warnings": warning_count,
                "info": info_count
            },
            "categories": {
                "python_issues": len(self.python_issues),
                "file_issues": len(self.file_issues),
                "dependency_issues": len(self.dependency_issues)
            },
            "all_issues": {
                "critical": self.critical_errors,
                "errors": self.issues,
                "warnings": self.warnings,
                "info": self.info
            }
        }
        
        with open("system_diagnostic_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved: system_diagnostic_report.json")
        print("=" * 70)
        
        return report_data

def main():
    """Main diagnostic function"""
    diagnostic = SystemDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()