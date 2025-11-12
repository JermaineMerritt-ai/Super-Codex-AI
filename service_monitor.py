#!/usr/bin/env python3
"""
Service Monitor - Eternal Flame Service Management
Provides service monitoring with auto-restart capabilities for the Super-Codex-AI system.
"""

import subprocess
import time
import threading
import signal
import sys
import argparse
import logging
import json
import os
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('service_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def monitor_service(cmd):
    """
    Simple service monitor that restarts a service when it dies.
    User-provided monitoring function.
    """
    while True:
        proc = subprocess.Popen(cmd)
        proc.wait()
        print("Service died, reigniting...")
        time.sleep(2)

class ServiceMonitor:
    """Enhanced service monitoring with logging, graceful shutdown, and threading support."""
    
    def __init__(self, service_name="Unknown Service", restart_delay=2):
        self.service_name = service_name
        self.restart_delay = restart_delay
        self.running = False
        self.current_process = None
        self.monitor_thread = None
        self.restart_count = 0
        self.start_time = None
        
        # Service directory management
        self.SERVICE_DIR = "services/"
        os.makedirs(self.SERVICE_DIR, exist_ok=True)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down {self.service_name} monitor...")
        self.stop()
        sys.exit(0)
    
    def _save_service_data(self, service_data):
        """Save service data to JSON file."""
        name = service_data.get('name', self.service_name).replace(' ', '_').lower()
        with open(os.path.join(self.SERVICE_DIR, f"{name}.json"), "w") as f:
            json.dump(service_data, f, indent=2)
        logger.info(f"Service data saved: {name}.json")
    
    def _load_service_data(self, name=None):
        """Load service data from JSON file."""
        if not name:
            name = self.service_name.replace(' ', '_').lower()
        
        service_file = os.path.join(self.SERVICE_DIR, f"{name}.json")
        if os.path.exists(service_file):
            with open(service_file, "r") as f:
                return json.load(f)
        return None
    
    def _monitor_loop(self, cmd):
        """Internal monitoring loop that runs in a separate thread."""
        logger.info(f"Starting monitoring loop for {self.service_name}")
        self.start_time = datetime.now()
        
        while self.running:
            try:
                logger.info(f"Starting {self.service_name} (restart #{self.restart_count})")
                
                # Start the service process
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for process to complete
                returncode = self.current_process.wait()
                
                if self.running:  # Only restart if we're still supposed to be running
                    self.restart_count += 1
                    logger.warning(f"{self.service_name} died with return code {returncode}, reigniting...")
                    print("Service died, reigniting...")
                    
                    # Log any output from the failed process
                    if self.current_process.stdout:
                        stdout = self.current_process.stdout.read()
                        if stdout:
                            logger.info(f"Service stdout: {stdout}")
                    
                    if self.current_process.stderr:
                        stderr = self.current_process.stderr.read()
                        if stderr:
                            logger.error(f"Service stderr: {stderr}")
                    
                    # Wait before restarting
                    time.sleep(self.restart_delay)
                else:
                    logger.info(f"{self.service_name} stopped normally")
                    break
                    
            except Exception as e:
                if self.running:
                    logger.error(f"Error monitoring {self.service_name}: {e}")
                    time.sleep(self.restart_delay)
                else:
                    break
    
    def start(self, cmd):
        """Start monitoring a service with the given command."""
        if self.running:
            logger.warning(f"{self.service_name} monitor is already running")
            return
        
        self.running = True
        self.restart_count = 0
        
        # Save service data
        service_data = {
            "name": self.service_name,
            "command": cmd,
            "start_time": datetime.now().isoformat(),
            "restart_delay": self.restart_delay,
            "status": "starting"
        }
        self._save_service_data(service_data)
        
        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(cmd,),
            daemon=True
        )
        self.monitor_thread.start()
        
        logger.info(f"Started monitoring {self.service_name}")
    
    def stop(self):
        """Stop monitoring and terminate the current service process."""
        logger.info(f"Stopping {self.service_name} monitor...")
        self.running = False
        
        # Terminate current process if running
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                # Give it a moment to shut down gracefully
                time.sleep(1)
                if self.current_process.poll() is None:
                    self.current_process.kill()
                logger.info(f"Terminated {self.service_name} process")
            except Exception as e:
                logger.error(f"Error terminating {self.service_name}: {e}")
        
        # Save final service data
        service_data = {
            "name": self.service_name,
            "status": "stopped",
            "stop_time": datetime.now().isoformat(),
            "restart_count": self.restart_count
        }
        self._save_service_data(service_data)
        
        # Wait for monitor thread to finish
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        logger.info(f"Stopped {self.service_name} monitor")
    
    def status(self):
        """Get current status of the monitored service."""
        if not self.running:
            return "Not monitoring"
        
        uptime = datetime.now() - self.start_time if self.start_time else None
        process_status = "Running" if (self.current_process and self.current_process.poll() is None) else "Not running"
        
        return {
            "service_name": self.service_name,
            "monitoring": self.running,
            "process_status": process_status,
            "restart_count": self.restart_count,
            "uptime": str(uptime) if uptime else "N/A",
            "process_id": self.current_process.pid if self.current_process else None
        }

def main():
    """Command-line interface for the service monitor."""
    parser = argparse.ArgumentParser(description="Service Monitor - Eternal Flame Management")
    parser.add_argument("--simple", action="store_true", help="Use simple monitor function")
    parser.add_argument("--name", default="Service", help="Service name for logging")
    parser.add_argument("--delay", type=int, default=2, help="Restart delay in seconds")
    parser.add_argument("command", nargs="+", help="Command to monitor")
    
    args = parser.parse_args()
    
    if args.simple:
        # Use the simple monitor function provided by user
        logger.info(f"Starting simple monitor for command: {' '.join(args.command)}")
        monitor_service(args.command)
    else:
        # Use the enhanced ServiceMonitor class
        monitor = ServiceMonitor(service_name=args.name, restart_delay=args.delay)
        
        try:
            logger.info(f"Starting enhanced monitor for {args.name}: {' '.join(args.command)}")
            monitor.start(args.command)
            
            # Keep the main thread alive
            while monitor.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            monitor.stop()

if __name__ == "__main__":
    main()