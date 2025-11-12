#!/usr/bin/env python3
"""
SystemD Crown - Eternal Flame Service Management
Sacred service orchestration system for the Super-Codex-AI dominion.
Provides systemd-inspired service management with eternal flame metaphors.
"""

import os
import sys
import json
import time
import signal
import subprocess
import threading
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any

# Service states
SERVICE_STATES = {
    "IGNITED": "ignited",      # Service is running
    "EXTINGUISHED": "extinguished",  # Service is stopped
    "KINDLING": "kindling",    # Service is starting
    "SMOLDERING": "smoldering", # Service is failing
    "CONSECRATED": "consecrated"  # Service is blessed/protected
}

@dataclass
class ServiceFlame:
    """Represents a service managed by the Systemd Crown."""
    service_id: str
    name: str
    command: List[str]
    working_directory: str
    state: str
    pid: Optional[int] = None
    start_time: Optional[str] = None
    restart_count: int = 0
    auto_restart: bool = True
    environment: Dict[str, str] = None
    
    def __post_init__(self):
        if self.environment is None:
            self.environment = {}

class SystemdCrown:
    """Sacred service management system with eternal flame capabilities."""
    
    def __init__(self, storage_dir: str = None):
        self.storage_dir = Path(storage_dir or "./systemd_crown_storage")
        self.storage_dir.mkdir(exist_ok=True)
        
        # Service storage paths
        self.services_dir = self.storage_dir / "services"
        self.logs_dir = self.storage_dir / "logs"
        self.beacons_dir = self.storage_dir / "beacons"  # Inheritance beacons
        
        for directory in [self.services_dir, self.logs_dir, self.beacons_dir]:
            directory.mkdir(exist_ok=True)
        
        # Active services and monitoring
        self.active_services: Dict[str, ServiceFlame] = {}
        self.service_processes: Dict[str, subprocess.Popen] = {}
        self.monitor_threads: Dict[str, threading.Thread] = {}
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Load existing services
        self._load_services()
        
        print("🔥 SystemD Crown initialized - Eternal flames await ignition")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n⚡ Received signal {signum} - Initiating graceful shutdown of all flames")
        self.shutdown_all()
        sys.exit(0)
    
    def _generate_service_id(self, prefix: str = "FS") -> str:
        """Generate a unique service ID with ceremonial prefix."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"{prefix}-{timestamp}-{unique_id}"
    
    def _save_service(self, service: ServiceFlame):
        """Save service configuration to persistent storage."""
        service_file = self.services_dir / f"{service.service_id}.json"
        with open(service_file, 'w') as f:
            json.dump(asdict(service), f, indent=2)
    
    def _load_services(self):
        """Load services from persistent storage."""
        for service_file in self.services_dir.glob("*.json"):
            try:
                with open(service_file, 'r') as f:
                    service_data = json.load(f)
                    service = ServiceFlame(**service_data)
                    self.active_services[service.service_id] = service
                    print(f"📜 Loaded service flame: {service.name} ({service.service_id})")
            except Exception as e:
                print(f"❌ Failed to load service from {service_file}: {e}")
    
    def _start_service(self, service: ServiceFlame) -> bool:
        """Start a service process."""
        try:
            print(f"🔥 Igniting eternal flame: {service.name}")
            
            # Prepare environment
            env = os.environ.copy()
            env.update(service.environment)
            
            # Handle command execution - fix for space-separated commands
            if len(service.command) == 1 and ' ' in service.command[0]:
                # Split space-separated command into list
                cmd_parts = service.command[0].split()
            else:
                cmd_parts = service.command
            
            # Start the process
            process = subprocess.Popen(
                cmd_parts,
                cwd=service.working_directory,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Update service state
            service.state = SERVICE_STATES["IGNITED"]
            service.pid = process.pid
            service.start_time = datetime.now().isoformat()
            
            # Store process reference
            self.service_processes[service.service_id] = process
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_service,
                args=(service,),
                daemon=True
            )
            monitor_thread.start()
            self.monitor_threads[service.service_id] = monitor_thread
            
            # Save updated service state
            self._save_service(service)
            
            print(f"✨ Eternal flame ignited: {service.name} (PID: {process.pid})")
            return True
            
        except Exception as e:
            service.state = SERVICE_STATES["SMOLDERING"]
            self._save_service(service)
            print(f"💥 Failed to ignite {service.name}: {e}")
            return False
    
    def _monitor_service(self, service: ServiceFlame):
        """Monitor a service and handle restarts."""
        process = self.service_processes.get(service.service_id)
        if not process:
            return
        
        try:
            # Wait for process to complete
            returncode = process.wait()
            
            if self.running and service.auto_restart:
                service.restart_count += 1
                service.state = SERVICE_STATES["KINDLING"]
                self._save_service(service)
                
                print(f"🔥 Flame extinguished: {service.name} (exit: {returncode})")
                print(f"⚡ Triggering self-healing protocols (restart #{service.restart_count})")
                
                # Log the restart
                self._log_service_event(service, f"Service restarted (exit code: {returncode})")
                
                # Wait before restart
                time.sleep(2)
                
                # Restart the service
                self._start_service(service)
            else:
                service.state = SERVICE_STATES["EXTINGUISHED"]
                service.pid = None
                self._save_service(service)
                print(f"🌫️ Flame extinguished: {service.name} (monitoring disabled)")
                
        except Exception as e:
            service.state = SERVICE_STATES["SMOLDERING"]
            self._save_service(service)
            print(f"💥 Monitor error for {service.name}: {e}")
    
    def _log_service_event(self, service: ServiceFlame, event: str):
        """Log service events to file."""
        log_file = self.logs_dir / f"{service.service_id}.log"
        timestamp = datetime.now().isoformat()
        
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {event}\n")
    
    def _trigger_self_healing(self, service: ServiceFlame):
        """Trigger self-healing protocols for a service."""
        print(f"🔮 Initiating self-healing for {service.name}")
        
        # Create inheritance beacon
        beacon = {
            "beacon_id": self._generate_service_id("IB"),
            "service_id": service.service_id,
            "timestamp": datetime.now().isoformat(),
            "healing_level": "Sovereign Restoration", 
            "protocol": "Eternal Flame Renewal",
            "restart_count": service.restart_count
        }
        
        beacon_file = self.beacons_dir / f"{beacon['beacon_id']}.json"
        with open(beacon_file, 'w') as f:
            json.dump(beacon, f, indent=2)
        
        print(f"🏺 Inheritance beacon created: {beacon['beacon_id']}")
    
    def ignite_eternal_flame(self, name: str, command: List[str], 
                           working_dir: str = None, 
                           auto_restart: bool = True,
                           environment: Dict[str, str] = None) -> str:
        """Ignite a new eternal flame service."""
        
        service_id = self._generate_service_id("FS")  # Flame Service
        working_dir = working_dir or os.getcwd()
        
        service = ServiceFlame(
            service_id=service_id,
            name=name,
            command=command,
            working_directory=working_dir,
            state=SERVICE_STATES["KINDLING"],
            auto_restart=auto_restart,
            environment=environment or {}
        )
        
        # Store service
        self.active_services[service_id] = service
        self._save_service(service)
        
        # Start the service
        if self._start_service(service):
            # Trigger self-healing beacon
            self._trigger_self_healing(service)
            return service_id
        else:
            return None
    
    def extinguish_flame(self, service_id: str) -> bool:
        """Extinguish a service flame."""
        service = self.active_services.get(service_id)
        if not service:
            print(f"❌ Service not found: {service_id}")
            return False
        
        print(f"🌫️ Extinguishing flame: {service.name}")
        
        # Stop monitoring
        service.auto_restart = False
        
        # Terminate process
        process = self.service_processes.get(service_id)
        if process and process.poll() is None:
            try:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
                print(f"⚰️ Process terminated: {service.name}")
            except Exception as e:
                print(f"💥 Error terminating {service.name}: {e}")
        
        # Update service state
        service.state = SERVICE_STATES["EXTINGUISHED"]
        service.pid = None
        self._save_service(service)
        
        # Log the event
        self._log_service_event(service, "Service manually extinguished")
        
        return True
    
    def list_flames(self) -> List[Dict[str, Any]]:
        """List all service flames and their status."""
        flames = []
        
        for service_id, service in self.active_services.items():
            process = self.service_processes.get(service_id)
            
            flame_info = {
                "service_id": service_id,
                "name": service.name,
                "state": service.state,
                "pid": service.pid,
                "start_time": service.start_time,
                "restart_count": service.restart_count,
                "auto_restart": service.auto_restart,
                "process_alive": process.poll() is None if process else False,
                "command": " ".join(service.command)
            }
            
            flames.append(flame_info)
        
        return flames
    
    def flame_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a specific flame."""
        service = self.active_services.get(service_id)
        if not service:
            return None
        
        process = self.service_processes.get(service_id)
        
        # Calculate uptime
        uptime = None
        if service.start_time:
            start = datetime.fromisoformat(service.start_time)
            uptime = str(datetime.now() - start)
        
        return {
            "service_id": service_id,
            "name": service.name,
            "state": service.state,
            "pid": service.pid,
            "command": service.command,
            "working_directory": service.working_directory,
            "start_time": service.start_time,
            "uptime": uptime,
            "restart_count": service.restart_count,
            "auto_restart": service.auto_restart,
            "process_alive": process.poll() is None if process else False,
            "environment": service.environment
        }
    
    def consecrate_flame(self, service_id: str) -> bool:
        """Consecrate a flame to prevent auto-restart (for critical services)."""
        service = self.active_services.get(service_id)
        if not service:
            return False
        
        service.state = SERVICE_STATES["CONSECRATED"]
        service.auto_restart = False  # Consecrated flames don't auto-restart
        self._save_service(service)
        
        print(f"🏆⭐ Flame consecrated: {service.name} - Protected from automatic restart")
        self._log_service_event(service, "Service consecrated - auto-restart disabled")
        return True
    
    def shutdown_all(self):
        """Shutdown all services gracefully."""
        print("🌫️ Extinguishing all eternal flames...")
        self.running = False
        
        for service_id in list(self.active_services.keys()):
            self.extinguish_flame(service_id)
        
        print("🌙 All flames extinguished - SystemD Crown dormant")

def main():
    """Command-line interface for SystemD Crown."""
    parser = argparse.ArgumentParser(description="SystemD Crown - Eternal Flame Service Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ignite command
    ignite_parser = subparsers.add_parser('ignite', help='Ignite a new eternal flame')
    ignite_parser.add_argument('name', help='Service name')
    ignite_parser.add_argument('command', nargs='+', help='Command to run')
    ignite_parser.add_argument('--dir', help='Working directory')
    ignite_parser.add_argument('--no-restart', action='store_true', help='Disable auto-restart')
    
    # List command  
    subparsers.add_parser('list', help='List all flames')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get flame status')
    status_parser.add_argument('service_id', help='Service ID')
    
    # Extinguish command
    extinguish_parser = subparsers.add_parser('extinguish', help='Extinguish a flame')
    extinguish_parser.add_argument('service_id', help='Service ID')
    
    # Consecrate command
    consecrate_parser = subparsers.add_parser('consecrate', help='Consecrate a flame')
    consecrate_parser.add_argument('service_id', help='Service ID')
    
    # Quick ignite for common services
    parser.add_argument('--ignite', metavar='SERVICE_NAME', help='Quick ignite with auto-detected command')
    
    args = parser.parse_args()
    
    # Initialize SystemD Crown
    crown = SystemdCrown()
    
    if args.command == 'ignite':
        service_id = crown.ignite_eternal_flame(
            name=args.name,
            command=args.command,
            working_dir=args.dir,
            auto_restart=not args.no_restart
        )
        if service_id:
            print(f"🔥 Service ignited: {service_id}")
        else:
            print("💥 Failed to ignite service")
            sys.exit(1)
    
    elif args.command == 'list':
        flames = crown.list_flames()
        if flames:
            print("\n🔥 Eternal Flames Status:")
            print("-" * 80)
            for flame in flames:
                status_icon = "🔥" if flame['process_alive'] else "🌫️"
                print(f"{status_icon} {flame['name']:<20} | {flame['service_id']:<20} | {flame['state']:<12} | PID: {flame['pid'] or 'N/A'}")
        else:
            print("🌫️ No eternal flames currently burning")
    
    elif args.command == 'status':
        status = crown.flame_status(args.service_id)
        if status:
            print(f"\n🔥 Flame Status: {status['name']}")
            print("-" * 50)
            for key, value in status.items():
                print(f"{key:<20}: {value}")
        else:
            print(f"❌ Service not found: {args.service_id}")
    
    elif args.command == 'extinguish':
        if crown.extinguish_flame(args.service_id):
            print(f"🌫️ Flame extinguished: {args.service_id}")
        else:
            print(f"❌ Failed to extinguish: {args.service_id}")
    
    elif args.command == 'consecrate':
        if crown.consecrate_flame(args.service_id):
            print(f"🏆 Flame consecrated: {args.service_id}")
        else:
            print(f"❌ Failed to consecrate: {args.service_id}")
    
    elif args.ignite:
        # Quick ignite for common services
        service_name = args.ignite
        if service_name.lower() == "axiom-flame":
            # Auto-detect Flask API
            api_path = "C:\\Users\\JMerr\\OneDrive\\Documents\\.vscode\\codex_project\\backend\\services\\dominion\\Super-Codex-AI\\axiom-flame\\packages\\api"
            service_id = crown.ignite_eternal_flame(
                name="Axiom Flame API",
                command=["python", "app.py"],
                working_dir=api_path
            )
            if service_id:
                print(f"🔥 Axiom Flame API ignited: {service_id}")
            else:
                print("💥 Failed to ignite Axiom Flame API")
        else:
            print(f"❌ Unknown service for quick ignite: {service_name}")
    
    else:
        # Interactive mode
        print("🔥 SystemD Crown - Interactive Mode")
        print("Available commands: ignite, list, status, extinguish, consecrate, quit")
        
        while True:
            try:
                cmd = input("\n👑 Crown> ").strip().split()
                if not cmd:
                    continue
                
                if cmd[0] == 'quit' or cmd[0] == 'exit':
                    break
                elif cmd[0] == 'list':
                    flames = crown.list_flames()
                    if flames:
                        print("\n🔥 Eternal Flames:")
                        for flame in flames:
                            status_icon = "🔥" if flame['process_alive'] else "🌫️"
                            print(f"  {status_icon} {flame['name']} ({flame['service_id']}) - {flame['state']}")
                    else:
                        print("🌫️ No flames burning")
                else:
                    print("❓ Unknown command. Available: ignite, list, status, extinguish, consecrate, quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"💥 Error: {e}")
        
        crown.shutdown_all()

if __name__ == "__main__":
    main()