#!/usr/bin/env python3
"""
System Diagnostic and Fix Script for Super-Codex-AI
Identifies and fixes all system issues
"""

import os
import sys
import json
import traceback
from pathlib import Path

# Add paths to system path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))
sys.path.insert(0, str(project_root / "app"))

class SystemDiagnostic:
    def __init__(self):
        self.issues = []
        self.fixes_applied = []
        
    def log_issue(self, component, description, severity="ERROR"):
        self.issues.append({
            "component": component,
            "description": description,
            "severity": severity
        })
        print(f"[{severity}] {component}: {description}")
        
    def log_fix(self, component, description):
        self.fixes_applied.append({
            "component": component,
            "fix": description
        })
        print(f"[FIX] {component}: {description}")
        
    def test_backend_imports(self):
        """Test if backend modules can be imported"""
        print("\\n=== Testing Backend Imports ===")
        
        # Test FastAPI app import
        try:
            from backend.main import app
            print("✅ Backend main app imports successfully")
        except Exception as e:
            self.log_issue("Backend Main", f"Cannot import main app: {e}")
            
        # Test app modules
        try:
            from app.auth import User, get_user, require_admin
            print("✅ App auth modules import successfully")
        except Exception as e:
            self.log_issue("App Auth", f"Cannot import auth modules: {e}")
            
        # Test database
        try:
            from app.db import engine, Base
            print("✅ Database modules import successfully")
        except Exception as e:
            self.log_issue("Database", f"Cannot import database modules: {e}")
            
        # Test API modules
        try:
            from backend.api.webhooks import router
            print("✅ API webhooks import successfully")
        except Exception as e:
            self.log_issue("API Webhooks", f"Cannot import webhooks: {e}")
            
        try:
            from backend.api.upload import router
            print("✅ API upload imports successfully")  
        except Exception as e:
            self.log_issue("API Upload", f"Cannot import upload: {e}")
            
    def test_axiom_flame(self):
        """Test AXIOM Flame API"""
        print("\\n=== Testing AXIOM Flame ===")
        
        try:
            from axiom_flame.packages.api.app import create_app
            app = create_app()
            print("✅ AXIOM Flame app creates successfully")
        except Exception as e:
            self.log_issue("AXIOM Flame", f"Cannot create AXIOM app: {e}")
            
        # Test config
        try:
            from axiom_flame.packages.api.config import Config
            Config.init_directories()
            print("✅ AXIOM Flame config loads successfully")
        except Exception as e:
            self.log_issue("AXIOM Config", f"Cannot load AXIOM config: {e}")
            
    def test_frontend_setup(self):
        """Test frontend configuration"""
        print("\\n=== Testing Frontend Setup ===")
        
        frontend_path = project_root / "frontend"
        package_json = frontend_path / "package.json"
        
        if package_json.exists():
            print("✅ Frontend package.json exists")
            try:
                with open(package_json) as f:
                    config = json.load(f)
                if config.get("proxy") == "http://localhost:8010":
                    print("✅ Frontend proxy configured correctly")
                else:
                    self.log_issue("Frontend Config", f"Proxy misconfigured: {config.get('proxy')}")
            except Exception as e:
                self.log_issue("Frontend Config", f"Cannot read package.json: {e}")
        else:
            self.log_issue("Frontend Setup", "package.json not found")
            
        # Check if node_modules exists
        node_modules = frontend_path / "node_modules"
        if node_modules.exists():
            print("✅ Frontend dependencies installed")
        else:
            self.log_issue("Frontend Deps", "Node modules not installed", "WARNING")
            
    def test_file_structure(self):
        """Test required file structure"""
        print("\\n=== Testing File Structure ===")
        
        required_files = [
            "backend/main.py",
            "backend/api/__init__.py", 
            "backend/api/webhooks.py",
            "backend/api/upload.py",
            "app/__init__.py",
            "app/main.py",
            "app/auth.py",
            "app/db.py",
            "app/models.py",
            "axiom-flame/packages/api/app.py",
            "axiom-flame/packages/api/config.py",
            "axiom-flame/packages/api/routes.py",
            "frontend/package.json"
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                self.log_issue("File Structure", f"Missing required file: {file_path}")
                
    def fix_missing_imports(self):
        """Fix missing import files"""
        print("\\n=== Applying Import Fixes ===")
        
        # Create missing __init__.py files
        init_dirs = [
            "backend/services",
            "backend/services/dominion", 
            "axiom-flame",
            "axiom-flame/packages"
        ]
        
        for dir_path in init_dirs:
            init_file = project_root / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.parent.mkdir(parents=True, exist_ok=True)
                init_file.write_text("# Package init\\n")
                self.log_fix("Import Structure", f"Created {init_file}")
                
    def create_startup_script(self):
        """Create a working startup script"""
        print("\\n=== Creating Startup Script ===")
        
        startup_content = '''#!/usr/bin/env python3
"""
Super-Codex-AI Unified Startup Script
Starts all services in the correct order
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

project_root = Path(__file__).parent
os.chdir(project_root)

def start_backend():
    """Start the FastAPI backend"""
    print("Starting FastAPI backend on port 8010...")
    try:
        os.system(f"{sys.executable} -m uvicorn backend.main:app --host 127.0.0.1 --port 8010 --reload")
    except KeyboardInterrupt:
        print("Backend stopped")

def start_axiom_flame():
    """Start AXIOM Flame API"""
    print("Starting AXIOM Flame API on port 5010...")
    try:
        os.chdir("axiom-flame/packages/api")
        os.system(f"{sys.executable} app.py 5010")
    except KeyboardInterrupt:
        print("AXIOM Flame stopped")

def start_frontend():
    """Start React frontend"""
    print("Starting React frontend on port 3001...")
    try:
        os.chdir("frontend")
        os.environ["PORT"] = "3001"
        os.system("npm start")
    except KeyboardInterrupt:
        print("Frontend stopped")

def main():
    print("🚀 Starting Super-Codex-AI System")
    print("=================================")
    
    # Start services in separate threads
    services = [
        threading.Thread(target=start_axiom_flame, daemon=True),
        threading.Thread(target=start_backend, daemon=True),
        threading.Thread(target=start_frontend, daemon=True)
    ]
    
    for service in services:
        service.start()
        time.sleep(2)  # Stagger startup
    
    print("\\n✅ All services started!")
    print("Backend: http://127.0.0.1:8010")
    print("AXIOM Flame: http://127.0.0.1:5010") 
    print("Frontend: http://127.0.0.1:3001")
    print("\\nPress Ctrl+C to stop all services")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down all services...")
        os._exit(0)

if __name__ == "__main__":
    main()
'''
        
        startup_file = project_root / "start_system.py"
        startup_file.write_text(startup_content)
        self.log_fix("Startup Script", f"Created unified startup script: {startup_file}")
        
    def create_environment_file(self):
        """Create proper environment configuration"""
        print("\\n=== Creating Environment Configuration ===")
        
        env_content = '''# Super-Codex-AI Environment Configuration
# Core settings
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///./codex.db
DB_NAME=codex_db
DB_USER=codex_user
DB_PASSWORD=codex_pass

# Authentication
JWT_SECRET=super-secret-jwt-key-change-in-production
API_KEY=dev-api-key-12345
CLI_API_KEY=dev-cli-key-67890

# Services
BACKEND_PORT=8010
AXIOM_PORT=5010  
FRONTEND_PORT=3001

# CORS
CORS_ORIGINS=http://localhost:3001,http://127.0.0.1:3001

# Paths
UPLOAD_DIR=uploads
LOG_DIR=logs

# AXIOM Flame
AXIOM_BASE=http://127.0.0.1:5010
FLASK_HOST=127.0.0.1
FLASK_PORT=5010
FLASK_DEBUG=true
'''
        
        env_file = project_root / ".env"
        if not env_file.exists():
            env_file.write_text(env_content)
            self.log_fix("Environment", f"Created .env configuration")
        else:
            print("✅ .env file already exists")
            
    def fix_axiom_flame_port(self):
        """Fix AXIOM Flame port configuration"""
        print("\\n=== Fixing AXIOM Flame Port ===")
        
        config_file = project_root / "axiom-flame/packages/api/config.py"
        if config_file.exists():
            content = config_file.read_text()
            if "PORT = int(os.environ.get('FLASK_PORT', 8087))" in content:
                new_content = content.replace(
                    "PORT = int(os.environ.get('FLASK_PORT', 8087))",
                    "PORT = int(os.environ.get('FLASK_PORT', 5010))"
                )
                config_file.write_text(new_content)
                self.log_fix("AXIOM Port", "Fixed AXIOM Flame default port to 5010")
            else:
                print("✅ AXIOM Flame port already configured correctly")
                
    def run_diagnostic(self):
        """Run complete system diagnostic"""
        print("🔍 Super-Codex-AI System Diagnostic")
        print("===================================")
        
        # Test all components
        self.test_file_structure()
        self.test_backend_imports()
        self.test_axiom_flame()
        self.test_frontend_setup()
        
        # Apply fixes
        self.fix_missing_imports()
        self.create_environment_file()
        self.create_startup_script()
        self.fix_axiom_flame_port()
        
        # Summary
        print("\\n📋 Diagnostic Summary")
        print("=====================")
        print(f"Issues found: {len(self.issues)}")
        print(f"Fixes applied: {len(self.fixes_applied)}")
        
        if self.issues:
            print("\\n❌ Issues found:")
            for issue in self.issues:
                print(f"  - {issue['component']}: {issue['description']}")
                
        if self.fixes_applied:
            print("\\n✅ Fixes applied:")
            for fix in self.fixes_applied:
                print(f"  - {fix['component']}: {fix['fix']}")
                
        if len(self.issues) == 0:
            print("\\n🎉 System is healthy! No critical issues found.")
            print("\\nTo start the system, run:")
            print("  python start_system.py")
        else:
            print(f"\\n⚠️  {len([i for i in self.issues if i['severity'] == 'ERROR'])} critical issues remain")
            print("Review the issues above and fix manually if needed.")

if __name__ == "__main__":
    diagnostic = SystemDiagnostic()
    try:
        diagnostic.run_diagnostic()
    except Exception as e:
        print(f"\\n💥 Diagnostic failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)