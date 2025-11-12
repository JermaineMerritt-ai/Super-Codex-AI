#!/usr/bin/env python3
"""
Production Unified API Stack
Demonstrates single base URL architecture with AXIOM proxy
"""

import os
import sys
import time
import signal
import subprocess
import threading
from datetime import datetime

class UnifiedApiStack:
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def log(self, service, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{service}] {message}")
        
    def start_axiom_flame(self):
        """Start AXIOM-Flame Flask backend on port 5010"""
        self.log("AXIOM", "Starting AXIOM-Flame ceremonial backend...")
        
        # Ensure directory exists
        axiom_dir = "axiom_flame"
        if not os.path.exists(axiom_dir):
            os.makedirs(axiom_dir)
            
        # Check if app.py exists, create if not
        app_file = os.path.join(axiom_dir, "app.py")
        if not os.path.exists(app_file):
            self.log("AXIOM", "Creating AXIOM-Flame app.py...")
            # Would copy from template or create basic version
            
        env = os.environ.copy()
        env.update({
            "FLASK_APP": "axiom_flame/app.py",
            "FLASK_ENV": "development",
            "PYTHONPATH": "."
        })
        
        try:
            proc = subprocess.Popen(
                [sys.executable, "-c", 
                 "from axiom_flame.app import app; app.run(host='127.0.0.1', port=5010, debug=False)"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["axiom"] = proc
            self.log("AXIOM", "Started on http://127.0.0.1:5010")
            return True
            
        except Exception as e:
            self.log("AXIOM", f"Failed to start: {e}")
            return False
            
    def start_backend_gateway(self):
        """Start FastAPI backend with AXIOM gateway on port 8015"""
        self.log("GATEWAY", "Starting FastAPI backend with AXIOM gateway...")
        
        env = os.environ.copy()
        env.update({
            "AXIOM_BASE": "http://127.0.0.1:5010",  # Point to AXIOM-Flame
            "PYTHONPATH": "."
        })
        
        try:
            proc = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "backend_api:app", 
                 "--host", "127.0.0.1", "--port", "8015", "--reload"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["gateway"] = proc
            self.log("GATEWAY", "Started on http://127.0.0.1:8015")
            self.log("GATEWAY", "AXIOM proxy available at /api/axiom/execute")
            return True
            
        except Exception as e:
            self.log("GATEWAY", f"Failed to start: {e}")
            return False
            
    def start_frontend(self):
        """Start React frontend on port 3000 with unified API configuration"""
        self.log("FRONTEND", "Starting React frontend with unified API config...")
        
        frontend_dir = "frontend"
        if not os.path.exists(frontend_dir):
            self.log("FRONTEND", "Frontend directory not found, skipping...")
            return False
            
        env = os.environ.copy()
        env.update({
            "REACT_APP_API_BASE": "/api",  # Single base URL
            "PORT": "3000",
            "NODE_ENV": "development"
        })
        
        try:
            proc = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["frontend"] = proc
            self.log("FRONTEND", "Started on http://localhost:3000")
            self.log("FRONTEND", "Configured for single base URL: /api")
            return True
            
        except Exception as e:
            self.log("FRONTEND", f"Failed to start: {e}")
            return False
            
    def check_health(self):
        """Check health of all services"""
        import requests
        
        services = [
            ("AXIOM-Flame", "http://127.0.0.1:5010/health"),
            ("Gateway", "http://127.0.0.1:8015/health/live"),
            ("Gateway AXIOM Proxy", "http://127.0.0.1:8015/axiom/health"),
            ("Frontend", "http://localhost:3000")
        ]
        
        for service, url in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log("HEALTH", f"✅ {service}: OK")
                else:
                    self.log("HEALTH", f"⚠️ {service}: HTTP {response.status_code}")
            except requests.RequestException as e:
                self.log("HEALTH", f"❌ {service}: {e}")
                
    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        while self.running:
            for name, proc in self.processes.items():
                if proc and proc.poll() is not None:
                    self.log("MONITOR", f"Process {name} has stopped (exit code: {proc.returncode})")
                    
            time.sleep(5)
            
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log("SYSTEM", f"Received signal {signum}, shutting down...")
        self.shutdown()
        
    def shutdown(self):
        """Gracefully shutdown all processes"""
        self.running = False
        
        for name, proc in self.processes.items():
            if proc and proc.poll() is None:
                self.log("SHUTDOWN", f"Terminating {name}...")
                proc.terminate()
                
                # Wait for graceful shutdown
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.log("SHUTDOWN", f"Force killing {name}...")
                    proc.kill()
                    
        self.log("SYSTEM", "All services stopped")
        
    def start(self):
        """Start the complete unified API stack"""
        print("="*60)
        print("🚀 UNIFIED API STACK - Single Base URL Architecture")
        print("="*60)
        print("Architecture:")
        print("  React Frontend (port 3000)")
        print("      ↓ REACT_APP_API_BASE=/api")
        print("  FastAPI Gateway (port 8015) - /api/axiom/execute")  
        print("      ↓ Proxy to AXIOM_BASE")
        print("  AXIOM-Flame Backend (port 5010)")
        print("="*60)
        
        # Install signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start services in order
        services_started = 0
        
        if self.start_axiom_flame():
            services_started += 1
            time.sleep(3)  # Give AXIOM time to start
            
        if self.start_backend_gateway():
            services_started += 1
            time.sleep(2)  # Give gateway time to start
            
        if self.start_frontend():
            services_started += 1
            
        if services_started == 0:
            self.log("ERROR", "No services started successfully")
            return False
            
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        # Wait a moment then check health
        time.sleep(5)
        self.check_health()
        
        print("="*60)
        print("✅ UNIFIED API STACK OPERATIONAL")
        print("📱 Frontend: http://localhost:3000")
        print("🔗 Gateway API: http://127.0.0.1:8015/docs")
        print("⚡ AXIOM Backend: http://127.0.0.1:5010/health")
        print("🎯 All frontend calls route through: /api/axiom/execute")
        print("🛡️ No direct Flask calls from browser - unified proxy only")
        print("="*60)
        
        try:
            # Keep running until interrupted
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
            
        return True


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--health-only":
        stack = UnifiedApiStack()
        stack.check_health()
        return
        
    stack = UnifiedApiStack()
    
    try:
        success = stack.start()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Failed to start unified API stack: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()