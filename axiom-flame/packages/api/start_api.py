#!/usr/bin/env python3
"""
Axiom-Flame API Startup Script
Sacred service management for ceremonial operations
"""
import os
import sys
import time
import signal
import subprocess
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

class AxiomFlameService:
    def __init__(self):
        self.api_path = Path(__file__).parent / "app.py"
        self.pid_file = Path(__file__).parent / "axiom-flame.pid"
        self.log_file = Path(__file__).parent / "axiom-flame.log"
        self.process = None
        
    def start(self, port=8087, daemon=False):
        """Start the Axiom-Flame API service."""
        if self.is_running():
            print("🔥 Axiom-Flame API is already running")
            return True
            
        print(f"🔥 Igniting Axiom-Flame API on port {port}...")
        
        try:
            if daemon:
                # Start as daemon process
                cmd = [sys.executable, str(self.api_path), str(port)]
                with open(self.log_file, 'a') as log:
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        start_new_session=True
                    )
                # Save PID
                with open(self.pid_file, 'w') as f:
                    f.write(str(self.process.pid))
                print(f"✅ Axiom-Flame API started as daemon (PID: {self.process.pid})")
            else:
                # Start in foreground
                os.execv(sys.executable, [sys.executable, str(self.api_path), str(port)])
                
        except Exception as e:
            print(f"❌ Failed to start Axiom-Flame API: {e}")
            return False
            
        return True
        
    def stop(self):
        """Stop the Axiom-Flame API service."""
        if not self.is_running():
            print("🔥 Axiom-Flame API is not running")
            return True
            
        try:
            pid = self.get_pid()
            if pid:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)
                if self.is_running():
                    os.kill(pid, signal.SIGKILL)
                    
                if self.pid_file.exists():
                    self.pid_file.unlink()
                    
                print("🔥 Axiom-Flame API extinguished")
                return True
        except Exception as e:
            print(f"❌ Failed to stop Axiom-Flame API: {e}")
            return False
            
    def status(self):
        """Check the status of the Axiom-Flame API service."""
        if self.is_running():
            pid = self.get_pid()
            print(f"🔥 Axiom-Flame API is running (PID: {pid})")
            return True
        else:
            print("🔥 Axiom-Flame API is not running")
            return False
            
    def restart(self, port=8087):
        """Restart the Axiom-Flame API service."""
        print("🔥 Restarting Axiom-Flame API...")
        self.stop()
        time.sleep(1)
        return self.start(port, daemon=True)
        
    def is_running(self):
        """Check if the service is running."""
        pid = self.get_pid()
        if not pid:
            return False
            
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
            
    def get_pid(self):
        """Get the PID of the running service."""
        if not self.pid_file.exists():
            return None
            
        try:
            with open(self.pid_file, 'r') as f:
                return int(f.read().strip())
        except (ValueError, FileNotFoundError):
            return None
            
    def logs(self, lines=50):
        """Show recent log entries."""
        if not self.log_file.exists():
            print("📋 No log file found")
            return
            
        try:
            with open(self.log_file, 'r') as f:
                log_lines = f.readlines()
                recent_lines = log_lines[-lines:] if len(log_lines) > lines else log_lines
                print("📋 Recent Axiom-Flame API logs:")
                print("".join(recent_lines))
        except Exception as e:
            print(f"❌ Failed to read logs: {e}")

def main():
    service = AxiomFlameService()
    
    if len(sys.argv) < 2:
        print("Usage: python start_api.py {start|stop|restart|status|logs} [--daemon] [port]")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    daemon = "--daemon" in sys.argv or "-d" in sys.argv
    
    # Extract port from arguments, excluding flags
    port = 8087
    for arg in sys.argv[2:]:
        if arg.isdigit():
            port = int(arg)
            break
    
    if command == "start":
        service.start(port, daemon)
    elif command == "stop":
        service.stop()
    elif command == "restart":
        service.restart(port)
    elif command == "status":
        service.status()
    elif command == "logs":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        service.logs(lines)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()