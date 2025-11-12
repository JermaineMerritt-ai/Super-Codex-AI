#!/usr/bin/env python3
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
        subprocess.run([sys.executable, "-m", "uvicorn", "backend.main:app", 
                       "--host", "127.0.0.1", "--port", "8010", "--reload"])
    except KeyboardInterrupt:
        print("Backend stopped")

def start_axiom_flame():
    """Start AXIOM Flame API"""
    print("Starting AXIOM Flame API on port 5010...")
    try:
        os.chdir("axiom-flame/packages/api")
        subprocess.run([sys.executable, "app.py", "5010"])
    except KeyboardInterrupt:
        print("AXIOM Flame stopped")
    finally:
        os.chdir(project_root)

def start_frontend():
    """Start React frontend"""
    print("Starting React frontend on port 3001...")
    try:
        os.chdir("frontend")
        env = os.environ.copy()
        env["PORT"] = "3001"
        subprocess.run(["npm", "start"], env=env)
    except KeyboardInterrupt:
        print("Frontend stopped")
    finally:
        os.chdir(project_root)

def main():
    print("Starting Super-Codex-AI System")
    print("===============================")
    
    # Start services in separate threads
    services = [
        threading.Thread(target=start_axiom_flame, daemon=True),
        threading.Thread(target=start_backend, daemon=True),
        threading.Thread(target=start_frontend, daemon=True)
    ]
    
    for service in services:
        service.start()
        time.sleep(2)  # Stagger startup
    
    print()
    print("All services started!")
    print("Backend: http://127.0.0.1:8010")
    print("AXIOM Flame: http://127.0.0.1:5010") 
    print("Frontend: http://127.0.0.1:3001")
    print()
    print("Press Ctrl+C to stop all services")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("Shutting down all services...")
        os._exit(0)

if __name__ == "__main__":
    main()
