#!/usr/bin/env python3
"""
AXIOM Integration Production Startup Script
Starts both AXIOM-Flame backend and FastAPI gateway with proper configuration
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path

# Configuration
AXIOM_PORT = 5010
GATEWAY_PORT = 8015
PROJECT_ROOT = Path(__file__).parent

class AxiomStack:
    def __init__(self):
        self.axiom_process = None
        self.gateway_process = None
        self.running = True
        
    def start_axiom_flame(self):
        """Start AXIOM-Flame Flask backend"""
        print("🔥 Starting AXIOM-Flame Flask Backend...")
        
        axiom_dir = PROJECT_ROOT / "axiom_flame"
        
        try:
            env = os.environ.copy()
            env["PORT"] = str(AXIOM_PORT)
            env["DEBUG"] = "false"
            
            self.axiom_process = subprocess.Popen(
                [sys.executable, "app.py"],
                cwd=axiom_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"   ✅ AXIOM-Flame started on port {AXIOM_PORT}")
            print(f"   📋 Process ID: {self.axiom_process.pid}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to start AXIOM-Flame: {e}")
            return False
    
    def start_gateway(self):
        """Start FastAPI Gateway"""
        print("🌉 Starting FastAPI Gateway...")
        
        try:
            env = os.environ.copy()
            env["AXIOM_BASE"] = f"http://localhost:{AXIOM_PORT}"
            
            self.gateway_process = subprocess.Popen([
                sys.executable, "-c",
                f"import uvicorn; from backend_api import app; uvicorn.run(app, host='127.0.0.1', port={GATEWAY_PORT}, log_level='info')"
            ],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
            )
            
            print(f"   ✅ FastAPI Gateway started on port {GATEWAY_PORT}")
            print(f"   📋 Process ID: {self.gateway_process.pid}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to start FastAPI Gateway: {e}")
            return False
    
    def wait_for_service(self, url, service_name, max_attempts=10):
        """Wait for a service to become available"""
        import requests
        
        print(f"⏳ Waiting for {service_name} to be ready...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    print(f"   ✅ {service_name} is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
                
            time.sleep(1)
            print(f"   ⏳ Attempt {attempt + 1}/{max_attempts}...")
            
        print(f"   ❌ {service_name} failed to start within timeout")
        return False
    
    def monitor_processes(self):
        """Monitor running processes and restart if needed"""
        print("👀 Starting process monitor...")
        
        while self.running:
            if self.axiom_process and self.axiom_process.poll() is not None:
                print("⚠️  AXIOM-Flame process died, restarting...")
                self.start_axiom_flame()
                
            if self.gateway_process and self.gateway_process.poll() is not None:
                print("⚠️  FastAPI Gateway process died, restarting...")
                self.start_gateway()
                
            time.sleep(5)
    
    def stop(self):
        """Stop all processes"""
        print("\\n🛑 Shutting down AXIOM Integration Stack...")
        
        self.running = False
        
        if self.gateway_process:
            print("   🌉 Stopping FastAPI Gateway...")
            self.gateway_process.terminate()
            try:
                self.gateway_process.wait(timeout=5)
                print("   ✅ FastAPI Gateway stopped")
            except subprocess.TimeoutExpired:
                print("   🔥 Force killing FastAPI Gateway...")
                self.gateway_process.kill()
                
        if self.axiom_process:
            print("   🔥 Stopping AXIOM-Flame...")
            self.axiom_process.terminate()
            try:
                self.axiom_process.wait(timeout=5)
                print("   ✅ AXIOM-Flame stopped")
            except subprocess.TimeoutExpired:
                print("   🔥 Force killing AXIOM-Flame...")
                self.axiom_process.kill()
        
        print("✅ AXIOM Integration Stack shutdown complete")
    
    def start(self):
        """Start the complete AXIOM integration stack"""
        print("🚀 Starting AXIOM Integration Stack...")
        print("=" * 60)
        
        # Start AXIOM-Flame first
        if not self.start_axiom_flame():
            return False
            
        # Wait for AXIOM-Flame to be ready
        if not self.wait_for_service(f"http://127.0.0.1:{AXIOM_PORT}/health", "AXIOM-Flame"):
            self.stop()
            return False
            
        # Start Gateway
        if not self.start_gateway():
            self.stop()
            return False
            
        # Wait for Gateway to be ready
        if not self.wait_for_service(f"http://127.0.0.1:{GATEWAY_PORT}/axiom/health", "FastAPI Gateway"):
            self.stop()
            return False
        
        print("\\n" + "=" * 60)
        print("🎉 AXIOM Integration Stack is READY!")
        print(f"🔥 AXIOM-Flame Backend: http://127.0.0.1:{AXIOM_PORT}")
        print(f"🌉 FastAPI Gateway: http://127.0.0.1:{GATEWAY_PORT}")
        print("=" * 60)
        print("\\n📋 Available Endpoints:")
        print(f"   🏥 Health Check: GET  {GATEWAY_PORT}/axiom/health")
        print(f"   🧠 Reasoning:    POST {GATEWAY_PORT}/axiom/reason")
        print(f"   🏆 Grant Honor:  POST {GATEWAY_PORT}/axiom/grant")
        print(f"   📜 Ceremonies:   GET  {GATEWAY_PORT}/axiom/ceremonies")
        print(f"   ⚡ Execute:      POST {GATEWAY_PORT}/axiom/execute")
        print("\\n🔄 Press Ctrl+C to stop...")
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        return True

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\\n🛑 Received shutdown signal...")
    if 'stack' in globals():
        stack.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the AXIOM stack
    stack = AxiomStack()
    
    try:
        if stack.start():
            # Keep running until interrupted
            while stack.running:
                time.sleep(1)
        else:
            print("❌ Failed to start AXIOM Integration Stack")
            sys.exit(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        stack.stop()