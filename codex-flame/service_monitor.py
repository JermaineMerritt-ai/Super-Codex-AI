#!/usr/bin/env python3
"""
🔥 Simple Service Monitor 🔥
Basic service monitoring and auto-restart functionality
"""

import subprocess
import time
import sys
import signal
import threading
from pathlib import Path

class ServiceMonitor:
    def __init__(self):
        self.running = True
        self.processes = {}
        
    def monitor_service(self, cmd, service_name=None, restart_delay=2):
        """
        Monitor a service and restart it if it dies
        
        Args:
            cmd: Command to run (list or string)
            service_name: Optional name for the service
            restart_delay: Seconds to wait before restarting
        """
        if isinstance(cmd, str):
            cmd = cmd.split()
        
        if service_name is None:
            service_name = ' '.join(cmd)
        
        print(f"🔥 Starting monitoring for: {service_name}")
        
        while self.running:
            try:
                print(f"🚀 Starting service: {service_name}")
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                self.processes[service_name] = proc
                
                # Wait for process to complete
                return_code = proc.wait()
                
                if not self.running:
                    break
                    
                print(f"💀 Service died: {service_name} (exit code: {return_code})")
                print("🔥 Service died, reigniting...")
                
                # Clean up
                if service_name in self.processes:
                    del self.processes[service_name]
                
                # Wait before restarting
                time.sleep(restart_delay)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Stopping monitor for: {service_name}")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error monitoring {service_name}: {e}")
                time.sleep(restart_delay)
    
    def monitor_multiple_services(self, services):
        """
        Monitor multiple services concurrently
        
        Args:
            services: List of tuples (cmd, service_name, restart_delay)
        """
        threads = []
        
        for service_config in services:
            if len(service_config) == 2:
                cmd, service_name = service_config
                restart_delay = 2
            elif len(service_config) == 3:
                cmd, service_name, restart_delay = service_config
            else:
                cmd = service_config[0]
                service_name = None
                restart_delay = 2
            
            thread = threading.Thread(
                target=self.monitor_service,
                args=(cmd, service_name, restart_delay),
                daemon=False
            )
            thread.start()
            threads.append(thread)
        
        try:
            # Wait for all threads
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("\n🛑 Stopping all service monitors...")
            self.stop_all()
    
    def stop_all(self):
        """Stop all monitoring and terminate processes"""
        self.running = False
        
        for service_name, proc in self.processes.items():
            try:
                print(f"🛑 Terminating: {service_name}")
                proc.terminate()
                
                # Wait a bit for graceful shutdown
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"💥 Force killing: {service_name}")
                    proc.kill()
                    proc.wait()
                    
            except Exception as e:
                print(f"❌ Error stopping {service_name}: {e}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n🔔 Received signal {signum}")
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

def monitor_service(cmd):
    """
    Simple function to monitor a single service (matches your request)
    """
    while True:
        if isinstance(cmd, str):
            cmd = cmd.split()
        
        proc = subprocess.Popen(cmd)
        proc.wait()
        print("Service died, reigniting...")
        time.sleep(2)

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="🔥 Simple Service Monitor")
    parser.add_argument("command", nargs="+", help="Command to monitor")
    parser.add_argument("--name", type=str, help="Service name")
    parser.add_argument("--delay", type=int, default=2, help="Restart delay in seconds")
    parser.add_argument("--simple", action="store_true", help="Use simple monitor function")
    
    args = parser.parse_args()
    
    if args.simple:
        # Use the simple function you requested
        monitor_service(args.command)
    else:
        # Use the enhanced monitor
        monitor = ServiceMonitor()
        monitor.setup_signal_handlers()
        
        try:
            monitor.monitor_service(
                args.command, 
                args.name or ' '.join(args.command),
                args.delay
            )
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")
            monitor.stop_all()

if __name__ == "__main__":
    main()