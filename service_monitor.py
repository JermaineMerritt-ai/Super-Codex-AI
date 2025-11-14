#!/usr/bin/env python3
"""
Service Monitor for Super-Codex-AI
Monitors and manages system services with ceremonial logging
"""

import psutil
import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/service_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ServiceStatus:
    """Service status data structure"""
    name: str
    pid: Optional[int]
    status: str  # running, stopped, error, unknown
    cpu_percent: float
    memory_percent: float
    start_time: Optional[str]
    last_check: str
    error_message: Optional[str] = None

class ServiceMonitor:
    """Monitor and manage system services"""
    
    def __init__(self, config_path: str = "service_monitor_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.services_status: Dict[str, ServiceStatus] = {}
        
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)
    
    def load_config(self) -> Dict:
        """Load service monitor configuration"""
        default_config = {
            "check_interval": 30,  # seconds
            "services": {
                "super_codex_api": {
                    "command": ["python", "-m", "uvicorn", "simple_server:app"],
                    "working_dir": ".",
                    "port": 8080,
                    "expected_memory_mb": 200,
                    "restart_on_failure": True,
                    "max_restarts": 3
                },
                "axiom_flame_api": {
                    "command": ["python", "app.py"],
                    "working_dir": "axiom-flame/packages/api",
                    "port": 8095,
                    "expected_memory_mb": 100,
                    "restart_on_failure": True,
                    "max_restarts": 5
                },
                "ceremonial_interface": {
                    "command": ["python", "ceremonial_interface.py"],
                    "working_dir": ".",
                    "port": 8090,
                    "expected_memory_mb": 150,
                    "restart_on_failure": True,
                    "max_restarts": 3
                }
            },
            "alerts": {
                "high_memory_threshold": 80,  # percent
                "high_cpu_threshold": 85,     # percent
                "max_downtime_minutes": 5
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                # Create default config file
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return default_config
    
    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def find_service_processes(self, service_name: str) -> List[psutil.Process]:
        """Find processes for a specific service"""
        service_config = self.config["services"].get(service_name, {})
        command_parts = service_config.get("command", [])
        working_dir = service_config.get("working_dir", ".")
        
        matching_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
                try:
                    proc_info = proc.info
                    cmdline = proc_info.get('cmdline', [])
                    
                    # Check if command matches
                    if len(cmdline) >= len(command_parts):
                        cmd_match = all(
                            part in str(cmdline[i]) if i < len(cmdline) else False
                            for i, part in enumerate(command_parts)
                        )
                        
                        if cmd_match:
                            matching_processes.append(proc)
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        
        except Exception as e:
            logger.error(f"Error finding processes for {service_name}: {e}")
        
        return matching_processes
    
    def get_service_status(self, service_name: str) -> ServiceStatus:
        """Get current status of a service"""
        try:
            processes = self.find_service_processes(service_name)
            current_time = datetime.now().isoformat()
            
            if not processes:
                return ServiceStatus(
                    name=service_name,
                    pid=None,
                    status="stopped",
                    cpu_percent=0.0,
                    memory_percent=0.0,
                    start_time=None,
                    last_check=current_time
                )
            
            # Use the first matching process (most likely the main one)
            proc = processes[0]
            
            try:
                cpu_percent = proc.cpu_percent(interval=0.1)
                memory_percent = proc.memory_percent()
                start_time = datetime.fromtimestamp(proc.create_time()).isoformat()
                
                return ServiceStatus(
                    name=service_name,
                    pid=proc.pid,
                    status="running",
                    cpu_percent=cpu_percent,
                    memory_percent=memory_percent,
                    start_time=start_time,
                    last_check=current_time
                )
            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return ServiceStatus(
                    name=service_name,
                    pid=None,
                    status="error",
                    cpu_percent=0.0,
                    memory_percent=0.0,
                    start_time=None,
                    last_check=current_time,
                    error_message="Process access denied or no longer exists"
                )
        
        except Exception as e:
            logger.error(f"Error getting status for {service_name}: {e}")
            return ServiceStatus(
                name=service_name,
                pid=None,
                status="unknown",
                cpu_percent=0.0,
                memory_percent=0.0,
                start_time=None,
                last_check=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def check_all_services(self) -> Dict[str, ServiceStatus]:
        """Check status of all configured services"""
        logger.info("Performing service status check...")
        
        for service_name in self.config["services"].keys():
            status = self.get_service_status(service_name)
            self.services_status[service_name] = status
            
            # Log status changes
            if service_name in self.services_status:
                prev_status = self.services_status[service_name].status
                if status.status != prev_status:
                    logger.info(f"Service {service_name} status changed: {prev_status} -> {status.status}")
            
            # Check for alerts
            self.check_service_alerts(service_name, status)
        
        return self.services_status
    
    def check_service_alerts(self, service_name: str, status: ServiceStatus):
        """Check if service status triggers any alerts"""
        alerts = self.config.get("alerts", {})
        
        # High memory usage alert
        if status.memory_percent > alerts.get("high_memory_threshold", 80):
            logger.warning(f"HIGH MEMORY: {service_name} using {status.memory_percent:.1f}% memory")
        
        # High CPU usage alert
        if status.cpu_percent > alerts.get("high_cpu_threshold", 85):
            logger.warning(f"HIGH CPU: {service_name} using {status.cpu_percent:.1f}% CPU")
        
        # Service down alert
        if status.status in ["stopped", "error"]:
            logger.error(f"SERVICE DOWN: {service_name} is {status.status}")
            if status.error_message:
                logger.error(f"Error details: {status.error_message}")
    
    def restart_service(self, service_name: str) -> bool:
        """Attempt to restart a service"""
        logger.info(f"Attempting to restart service: {service_name}")
        
        try:
            service_config = self.config["services"].get(service_name, {})
            command = service_config.get("command", [])
            working_dir = service_config.get("working_dir", ".")
            
            if not command:
                logger.error(f"No command configured for service {service_name}")
                return False
            
            # Kill existing processes
            processes = self.find_service_processes(service_name)
            for proc in processes:
                try:
                    proc.terminate()
                    proc.wait(timeout=10)
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    try:
                        proc.kill()
                    except psutil.NoSuchProcess:
                        pass
            
            # Start new process
            import subprocess
            env = os.environ.copy()
            
            process = subprocess.Popen(
                command,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            logger.info(f"Service {service_name} restarted with PID: {process.pid}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to restart service {service_name}: {e}")
            return False
    
    def generate_report(self) -> Dict:
        """Generate comprehensive service status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "uptime_seconds": time.time() - psutil.boot_time()
            },
            "alerts": []
        }
        
        for service_name, status in self.services_status.items():
            report["services"][service_name] = asdict(status)
            
            # Add alerts to report
            if status.status in ["stopped", "error"]:
                report["alerts"].append({
                    "service": service_name,
                    "level": "critical",
                    "message": f"Service {service_name} is {status.status}"
                })
        
        return report
    
    def run_monitor_loop(self):
        """Run the main monitoring loop"""
        logger.info("Starting service monitor...")
        check_interval = self.config.get("check_interval", 30)
        
        try:
            while True:
                self.check_all_services()
                
                # Save status report
                report = self.generate_report()
                with open("logs/service_status_report.json", "w") as f:
                    json.dump(report, f, indent=2)
                
                logger.info(f"Service check completed. Next check in {check_interval} seconds.")
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            logger.info("Service monitor stopped by user")
        except Exception as e:
            logger.error(f"Service monitor error: {e}")
            raise

def main():
    """Main entry point"""
    monitor = ServiceMonitor()
    
    try:
        monitor.run_monitor_loop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())