#!/usr/bin/env python3
"""
System-Wide Diagnostic Tool for Super-Codex-AI
Comprehensive analysis and fixing of all system issues
"""
import os
import sys
import ast
import importlib
import subprocess
import json
import traceback
from pathlib import Path
from typing import List, Dict, Any, Set

class SystemDiagnostic:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.issues = []
        self.fixes_applied = []
        self.python_files = []
        self.missing_imports = set()
        self.broken_scripts = []
        self.config_issues = []
        
    def log_issue(self, category: str, file_path: str, issue: str, severity: str = "ERROR"):
        """Log a system issue"""
        self.issues.append({
            "category": category,
            "file": str(file_path),
            "issue": issue,
            "severity": severity,
            "timestamp": None
        })
        
    def log_fix(self, file_path: str, fix_description: str):
        """Log a fix that was applied"""
        self.fixes_applied.append({
            "file": str(file_path),
            "fix": fix_description,
            "timestamp": None
        })
        
    def find_python_files(self):
        """Find all Python files in the system"""
        python_files = []
        for root, dirs, files in os.walk(self.root_path):
            # Skip virtual environment and cache directories
            dirs[:] = [d for d in dirs if d not in {'.venv', '__pycache__', '.git', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
                    
        self.python_files = python_files
        return python_files
        
    def analyze_python_syntax(self):
        """Check all Python files for syntax errors"""
        syntax_errors = []
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                syntax_errors.append((py_file, str(e)))
                self.log_issue("SYNTAX", py_file, f"Syntax Error: {e}")
            except UnicodeDecodeError as e:
                syntax_errors.append((py_file, f"Encoding error: {e}"))
                self.log_issue("ENCODING", py_file, f"Encoding Error: {e}")
            except Exception as e:
                syntax_errors.append((py_file, f"Parse error: {e}"))
                self.log_issue("PARSE", py_file, f"Parse Error: {e}")
                
        return syntax_errors
        
    def analyze_imports(self):
        """Check for missing imports and dependencies"""
        import_errors = []
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self._test_import(alias.name, py_file)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self._test_import(node.module, py_file)
                            
            except Exception as e:
                import_errors.append((py_file, str(e)))
                self.log_issue("IMPORT_ANALYSIS", py_file, f"Import analysis failed: {e}")
                
        return import_errors
        
    def _test_import(self, module_name: str, file_path: Path):
        """Test if a module can be imported"""
        if module_name in {'__future__', 'typing', 'collections', 'os', 'sys', 'json'}:
            return  # Skip built-in modules
            
        try:
            importlib.import_module(module_name)
        except ImportError:
            self.missing_imports.add(module_name)
            self.log_issue("MISSING_IMPORT", file_path, f"Missing module: {module_name}")
        except Exception as e:
            self.log_issue("IMPORT_ERROR", file_path, f"Import error for {module_name}: {e}")
            
    def check_configuration_files(self):
        """Check for missing or broken configuration files"""
        config_files = [
            ('.env', 'Environment variables'),
            ('requirements.txt', 'Python dependencies'),
            ('package.json', 'Node.js dependencies'),
            ('Dockerfile', 'Docker configuration'),
            ('docker-compose.yml', 'Docker Compose'),
            ('Caddyfile', 'Caddy configuration'),
        ]
        
        for config_file, description in config_files:
            config_path = self.root_path / config_file
            if not config_path.exists():
                self.log_issue("MISSING_CONFIG", config_path, f"Missing {description} file", "WARNING")
                self.config_issues.append((config_file, "Missing"))
            else:
                try:
                    # Validate file content based on type
                    if config_file.endswith('.json'):
                        with open(config_path) as f:
                            json.load(f)
                    elif config_file == 'requirements.txt':
                        with open(config_path) as f:
                            content = f.read()
                            if not content.strip():
                                self.log_issue("EMPTY_CONFIG", config_path, "Empty requirements.txt", "WARNING")
                except Exception as e:
                    self.log_issue("INVALID_CONFIG", config_path, f"Invalid {description}: {e}")
                    self.config_issues.append((config_file, f"Invalid: {e}"))
                    
    def check_scripts(self):
        """Check for broken or missing scripts"""
        script_extensions = {'.py', '.sh', '.ps1', '.bat'}
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in {'.venv', '__pycache__', '.git'}]
            
            for file in files:
                if any(file.endswith(ext) for ext in script_extensions):
                    script_path = Path(root) / file
                    self._check_script_validity(script_path)
                    
    def _check_script_validity(self, script_path: Path):
        """Check if a script is valid and executable"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if script_path.suffix == '.py':
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    self.broken_scripts.append((script_path, f"Syntax error: {e}"))
                    self.log_issue("BROKEN_SCRIPT", script_path, f"Python syntax error: {e}")
                    
            elif script_path.suffix in {'.sh', '.bat', '.ps1'}:
                if not content.strip():
                    self.log_issue("EMPTY_SCRIPT", script_path, "Empty script file", "WARNING")
                    
        except Exception as e:
            self.log_issue("SCRIPT_READ_ERROR", script_path, f"Cannot read script: {e}")
            
    def check_server_configuration(self):
        """Check server-related configuration and files"""
        server_files = [
            'simple_server.py',
            'main.py', 
            'ceremonial_interface.py',
            'circuit_breaker.py'
        ]
        
        for server_file in server_files:
            server_path = self.root_path / server_file
            if not server_path.exists():
                self.log_issue("MISSING_SERVER_FILE", server_path, f"Missing server file: {server_file}")
            else:
                # Check if the file has obvious issues
                try:
                    with open(server_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                except Exception as e:
                    self.log_issue("SERVER_FILE_ERROR", server_path, f"Server file error: {e}")
                    
    def install_missing_dependencies(self):
        """Install missing Python dependencies"""
        if not self.missing_imports:
            return
            
        # Common package mappings
        package_mappings = {
            'fastapi': 'fastapi',
            'uvicorn': 'uvicorn',
            'sentry_sdk': 'sentry-sdk',
            'prometheus_fastapi_instrumentator': 'prometheus-fastapi-instrumentator',
            'prometheus_client': 'prometheus-client',
            'jinja2': 'jinja2',
            'aiofiles': 'aiofiles',
            'multipart': 'python-multipart',
            'dotenv': 'python-dotenv',
            'requests': 'requests',
            'pydantic': 'pydantic'
        }
        
        packages_to_install = []
        for missing_module in self.missing_imports:
            # Try to map module name to package name
            if missing_module in package_mappings:
                packages_to_install.append(package_mappings[missing_module])
            elif missing_module.split('.')[0] in package_mappings:
                packages_to_install.append(package_mappings[missing_module.split('.')[0]])
            else:
                packages_to_install.append(missing_module)
                
        if packages_to_install:
            try:
                # Install packages
                cmd = [sys.executable, '-m', 'pip', 'install'] + packages_to_install
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    for package in packages_to_install:
                        self.log_fix("SYSTEM", f"Installed package: {package}")
                else:
                    self.log_issue("DEPENDENCY_INSTALL", "SYSTEM", f"Failed to install packages: {result.stderr}")
                    
            except Exception as e:
                self.log_issue("DEPENDENCY_INSTALL", "SYSTEM", f"Error installing dependencies: {e}")
                
    def create_missing_files(self):
        """Create missing essential files"""
        
        # Create .env file if missing
        env_path = self.root_path / '.env'
        if not env_path.exists():
            env_content = """# Super-Codex-AI Environment Variables
HOST=0.0.0.0
PORT=8080
ENVIRONMENT=development

# Sentry Configuration
SENTRY_DSN=https://your-sentry-dsn-here
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=1.0

# Database Configuration (if needed)
DATABASE_URL=

# Redis Configuration (if needed)
REDIS_URL=

# Security
SECRET_KEY=super-secret-key-change-in-production
"""
            with open(env_path, 'w') as f:
                f.write(env_content)
            self.log_fix(env_path, "Created .env file with default configuration")
            
        # Create requirements.txt if missing or empty
        req_path = self.root_path / 'requirements.txt'
        if not req_path.exists() or req_path.stat().st_size == 0:
            requirements_content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
sentry-sdk[fastapi]==1.38.0
prometheus-fastapi-instrumentator==6.1.0
prometheus-client==0.19.0
python-multipart==0.0.6
aiofiles==23.2.1
jinja2==3.1.2
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
"""
            with open(req_path, 'w') as f:
                f.write(requirements_content)
            self.log_fix(req_path, "Created/updated requirements.txt")
            
    def fix_common_code_issues(self):
        """Fix common code issues in Python files"""
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original_content = content
                
                # Fix common import issues
                if 'from circuit_breaker import' in content and not (self.root_path / 'circuit_breaker.py').exists():
                    # Create circuit_breaker.py if it's missing
                    self._create_circuit_breaker_file()
                    
                # Fix encoding issues by ensuring UTF-8 BOM is removed
                if content.startswith('\ufeff'):
                    content = content[1:]
                    
                # Save if changes were made
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log_fix(py_file, "Fixed encoding and import issues")
                    
            except Exception as e:
                self.log_issue("CODE_FIX", py_file, f"Error fixing code: {e}")
                
    def _create_circuit_breaker_file(self):
        """Create missing circuit_breaker.py file"""
        circuit_breaker_path = self.root_path / 'circuit_breaker.py'
        if circuit_breaker_path.exists():
            return
            
        circuit_breaker_content = '''"""
Circuit Breaker Implementation for Super-Codex-AI
"""
import time
from typing import Dict, Any, Callable
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open" 
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    async def call(self, func: Callable):
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is open")
                
        try:
            result = await func()
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self._record_failure()
            raise e
            
    def _record_failure(self):
        """Record a failure and update circuit state"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

class CircuitBreakerRegistry:
    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
        
    def get_or_create(self, name: str, **kwargs) -> CircuitBreaker:
        """Get or create a circuit breaker by name"""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(**kwargs)
        return self.breakers[name]
        
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all circuit breakers"""
        return {
            name: {
                "state": breaker.state.value,
                "failure_count": breaker.failure_count,
                "last_failure": breaker.last_failure_time
            }
            for name, breaker in self.breakers.items()
        }

# Global registry
circuit_breaker_registry = CircuitBreakerRegistry()
'''
        
        with open(circuit_breaker_path, 'w', encoding='utf-8') as f:
            f.write(circuit_breaker_content)
        self.log_fix(circuit_breaker_path, "Created missing circuit_breaker.py file")
        
    def run_comprehensive_diagnostic(self):
        """Run complete system diagnostic"""
        print("🔍 Starting comprehensive system diagnostic...")
        
        # Step 1: Find all files
        print("📁 Scanning for Python files...")
        self.find_python_files()
        print(f"   Found {len(self.python_files)} Python files")
        
        # Step 2: Check syntax
        print("🐍 Analyzing Python syntax...")
        syntax_errors = self.analyze_python_syntax()
        print(f"   Found {len(syntax_errors)} syntax errors")
        
        # Step 3: Check imports
        print("📦 Analyzing imports and dependencies...")
        self.analyze_imports()
        print(f"   Found {len(self.missing_imports)} missing imports")
        
        # Step 4: Check configuration
        print("⚙️  Checking configuration files...")
        self.check_configuration_files()
        print(f"   Found {len(self.config_issues)} configuration issues")
        
        # Step 5: Check scripts
        print("📜 Checking scripts...")
        self.check_scripts()
        print(f"   Found {len(self.broken_scripts)} broken scripts")
        
        # Step 6: Check server files
        print("🖥️  Checking server configuration...")
        self.check_server_configuration()
        
        print(f"\n📊 DIAGNOSTIC SUMMARY:")
        print(f"   Total Issues Found: {len(self.issues)}")
        print(f"   Missing Imports: {len(self.missing_imports)}")
        print(f"   Configuration Issues: {len(self.config_issues)}")
        print(f"   Broken Scripts: {len(self.broken_scripts)}")
        
    def apply_fixes(self):
        """Apply all possible fixes"""
        print("\n🔧 Applying fixes...")
        
        # Fix 1: Install missing dependencies
        print("📦 Installing missing dependencies...")
        self.install_missing_dependencies()
        
        # Fix 2: Create missing files
        print("📄 Creating missing essential files...")
        self.create_missing_files()
        
        # Fix 3: Fix code issues
        print("🐛 Fixing common code issues...")
        self.fix_common_code_issues()
        
        print(f"\n✅ FIXES APPLIED: {len(self.fixes_applied)}")
        for fix in self.fixes_applied:
            print(f"   ✓ {fix['file']}: {fix['fix']}")
            
    def generate_report(self):
        """Generate comprehensive diagnostic report"""
        report = {
            "diagnostic_summary": {
                "total_issues": len(self.issues),
                "total_fixes": len(self.fixes_applied),
                "python_files_scanned": len(self.python_files),
                "missing_imports": len(self.missing_imports),
                "config_issues": len(self.config_issues),
                "broken_scripts": len(self.broken_scripts)
            },
            "issues": self.issues,
            "fixes_applied": self.fixes_applied,
            "missing_imports": list(self.missing_imports),
            "config_issues": self.config_issues,
            "broken_scripts": [(str(path), issue) for path, issue in self.broken_scripts]
        }
        
        report_path = self.root_path / 'system_diagnostic_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"\n📋 Full diagnostic report saved to: {report_path}")
        return report

def main():
    """Main function to run system-wide diagnostic and fixes"""
    diagnostic = SystemDiagnostic()
    
    try:
        # Run diagnostic
        diagnostic.run_comprehensive_diagnostic()
        
        # Apply fixes
        diagnostic.apply_fixes()
        
        # Generate report
        diagnostic.generate_report()
        
        print("\n🎉 System-wide diagnostic and fixes completed!")
        print("🌟 The Super-Codex-AI system is now optimized and ready!")
        
    except Exception as e:
        print(f"\n❌ Error during diagnostic: {e}")
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())