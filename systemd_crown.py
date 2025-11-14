#!/usr/bin/env python3
"""
SystemD Crown - Advanced Service Management System
Ceremonial service orchestration with governance controls
"""

import os
import json
import time
import logging
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/systemd_crown.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServiceState(Enum):
    """Service states"""
    IGNITED = "ignited"      # Running
    EXTINGUISHED = "extinguished"  # Stopped
    FLICKERING = "flickering"      # Starting/Stopping
    SMOLDERING = "smoldering"      # Error state
    UNKNOWN = "unknown"            # Cannot determine

@dataclass
class ServiceRecord:
    """Service record for ceremonial tracking"""
    service_id: str
    name: str
    command: List[str]
    working_directory: str
    state: ServiceState
    pid: Optional[int]
    start_time: Optional[str]
    restart_count: int
    auto_restart: bool
    environment: Dict[str, str]
    last_output: str = ""
    last_error: str = ""

class SystemDCrown:
    """Ceremonial service management system"""
    
    def __init__(self, storage_dir: str = "systemd_crown_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.services_dir = self.storage_dir / "services"
        self.services_dir.mkdir(exist_ok=True)
        self.logs_dir = self.storage_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.services: Dict[str, ServiceRecord] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        
        # Load existing services
        self.load_services()
    
    def generate_service_id(self, name: str) -> str:
        """Generate unique service ID"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        import hashlib
        hash_part = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8].upper()
        return f"FS-{timestamp}-{hash_part}"
    
    def ignite_service(self, name: str, command: List[str], 
                      working_directory: str = ".", 
                      auto_restart: bool = True,
                      environment: Dict[str, str] = None) -> str:
        """Ignite (start) a new service"""
        service_id = self.generate_service_id(name)
        
        try:
            # Prepare environment
            env = os.environ.copy()
            if environment:
                env.update(environment)
            
            # Start process
            process = subprocess.Popen(
                command,
                cwd=working_directory,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Create service record
            service_record = ServiceRecord(
                service_id=service_id,
                name=name,
                command=command,
                working_directory=working_directory,
                state=ServiceState.IGNITED,
                pid=process.pid,
                start_time=datetime.now().isoformat(),
                restart_count=0,
                auto_restart=auto_restart,
                environment=environment or {}
            )
            
            # Store service
            self.services[service_id] = service_record
            self.processes[service_id] = process
            self.save_service(service_record)
            
            logger.info(f"🔥 Service ignited: {name} (ID: {service_id}, PID: {process.pid})")
            return service_id
        
        except Exception as e:
            logger.error(f"Failed to ignite service {name}: {e}")
            raise
    
    def extinguish_service(self, service_id: str, force: bool = False) -> bool:
        """Extinguish (stop) a service"""
        try:
            if service_id not in self.services:
                logger.error(f"Service not found: {service_id}")
                return False
            
            service = self.services[service_id]
            process = self.processes.get(service_id)
            
            if not process:
                logger.warning(f"No active process for service {service_id}")
                service.state = ServiceState.EXTINGUISHED
                service.pid = None
                self.save_service(service)
                return True
            
            # Attempt graceful shutdown
            if not force:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Service {service_id} did not terminate gracefully, forcing...")
                    force = True
            
            # Force kill if needed
            if force:
                process.kill()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.error(f"Service {service_id} could not be killed")
                    return False
            
            # Update service record
            service.state = ServiceState.EXTINGUISHED
            service.pid = None
            self.save_service(service)
            
            # Clean up
            if service_id in self.processes:
                del self.processes[service_id]
            
            logger.info(f"💧 Service extinguished: {service.name} (ID: {service_id})")
            return True
        
        except Exception as e:
            logger.error(f"Failed to extinguish service {service_id}: {e}")
            return False
    
    def restart_service(self, service_id: str) -> bool:
        """Restart a service"""
        try:
            if service_id not in self.services:
                logger.error(f"Service not found: {service_id}")
                return False
            
            service = self.services[service_id]
            
            # Extinguish first
            self.extinguish_service(service_id)
            time.sleep(2)  # Brief pause
            
            # Re-ignite
            new_service_id = self.ignite_service(
                service.name,
                service.command,
                service.working_directory,
                service.auto_restart,
                service.environment
            )
            
            # Update restart count
            new_service = self.services[new_service_id]
            new_service.restart_count = service.restart_count + 1
            self.save_service(new_service)
            
            # Remove old service record
            if service_id != new_service_id:
                self.remove_service(service_id)
            
            logger.info(f"🔄 Service restarted: {service.name} (new ID: {new_service_id})")
            return True
        
        except Exception as e:
            logger.error(f"Failed to restart service {service_id}: {e}")
            return False
    
    def get_service_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed service status"""
        if service_id not in self.services:
            return None
        
        service = self.services[service_id]
        process = self.processes.get(service_id)
        
        status = asdict(service)
        
        if process:
            # Check if process is still running
            poll_result = process.poll()
            if poll_result is None:
                status["state"] = ServiceState.IGNITED.value
                status["running"] = True
            else:
                status["state"] = ServiceState.EXTINGUISHED.value
                status["running"] = False
                status["exit_code"] = poll_result
        else:
            status["running"] = False
        
        # Add runtime information
        if service.start_time:
            start_dt = datetime.fromisoformat(service.start_time)
            runtime = datetime.now() - start_dt
            status["runtime_seconds"] = int(runtime.total_seconds())
        
        return status
    
    def list_services(self) -> Dict[str, Dict[str, Any]]:
        """List all services with their status"""
        services_status = {}
        
        for service_id in self.services:
            services_status[service_id] = self.get_service_status(service_id)
        
        return services_status
    
    def monitor_services(self):
        """Monitor services and handle auto-restart"""
        for service_id, service in list(self.services.items()):
            if service.auto_restart and service.state == ServiceState.IGNITED:
                process = self.processes.get(service_id)
                
                if process and process.poll() is not None:
                    # Process has died, attempt restart
                    logger.warning(f"Service {service.name} died unexpectedly, restarting...")
                    self.restart_service(service_id)
    
    def save_service(self, service: ServiceRecord):
        """Save service record to disk"""
        try:
            service_file = self.services_dir / f"{service.service_id}.json"
            service_data = asdict(service)
            service_data["state"] = service.state.value  # Convert enum to string
            
            with open(service_file, 'w') as f:
                json.dump(service_data, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to save service {service.service_id}: {e}")
    
    def load_services(self):
        """Load services from disk"""
        try:
            for service_file in self.services_dir.glob("*.json"):
                with open(service_file, 'r') as f:
                    service_data = json.load(f)
                
                # Convert state back to enum
                service_data["state"] = ServiceState(service_data["state"])
                
                service = ServiceRecord(**service_data)
                self.services[service.service_id] = service
                
                # Services loaded from disk are considered extinguished
                service.state = ServiceState.EXTINGUISHED
                service.pid = None
        
        except Exception as e:
            logger.error(f"Failed to load services: {e}")
    
    def remove_service(self, service_id: str):
        """Remove service record"""
        try:
            # Remove from memory
            if service_id in self.services:
                del self.services[service_id]
            
            if service_id in self.processes:
                del self.processes[service_id]
            
            # Remove from disk
            service_file = self.services_dir / f"{service_id}.json"
            if service_file.exists():
                service_file.unlink()
            
            logger.info(f"Service record removed: {service_id}")
        
        except Exception as e:
            logger.error(f"Failed to remove service {service_id}: {e}")
    
    def ceremonial_report(self) -> Dict[str, Any]:
        """Generate ceremonial status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "crown_status": "majestic",
            "total_services": len(self.services),
            "ignited_services": len([s for s in self.services.values() if s.state == ServiceState.IGNITED]),
            "services": self.list_services(),
            "system_health": {
                "storage_path": str(self.storage_dir),
                "uptime": "eternal",
                "flame_eternal": True
            }
        }
        
        return report

def main():
    """Main ceremonial service manager"""
    crown = SystemDCrown()
    
    try:
        # Example service ignition
        if len(os.sys.argv) > 1:
            command = os.sys.argv[1]
            
            if command == "ignite":
                if len(os.sys.argv) < 4:
                    print("Usage: systemd_crown.py ignite <name> <command...>")
                    return 1
                
                name = os.sys.argv[2]
                cmd = os.sys.argv[3:]
                service_id = crown.ignite_service(name, cmd)
                print(f"Service ignited: {service_id}")
            
            elif command == "extinguish":
                if len(os.sys.argv) < 3:
                    print("Usage: systemd_crown.py extinguish <service_id>")
                    return 1
                
                service_id = os.sys.argv[2]
                if crown.extinguish_service(service_id):
                    print(f"Service extinguished: {service_id}")
                else:
                    print(f"Failed to extinguish service: {service_id}")
                    return 1
            
            elif command == "status":
                services = crown.list_services()
                print(json.dumps(services, indent=2))
            
            elif command == "report":
                report = crown.ceremonial_report()
                print(json.dumps(report, indent=2))
            
            elif command == "monitor":
                logger.info("Starting ceremonial service monitor...")
                try:
                    while True:
                        crown.monitor_services()
                        time.sleep(10)
                except KeyboardInterrupt:
                    logger.info("Monitor stopped by royal decree")
            
            else:
                print("Unknown command. Available: ignite, extinguish, status, report, monitor")
                return 1
        
        else:
            print("SystemD Crown - Ceremonial Service Management")
            print("Commands: ignite, extinguish, status, report, monitor")
    
    except Exception as e:
        logger.error(f"Crown error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())