#!/usr/bin/env python3
"""
Service Registry Manager - Centralized service data management
Provides unified service directory and JSON storage for all monitoring systems.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class ServiceRegistry:
    """Centralized registry for service management and persistence."""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or "./service_registry")
        self.SERVICE_DIR = self.base_dir / "services"
        self.LOGS_DIR = self.base_dir / "logs"
        self.SNAPSHOTS_DIR = self.base_dir / "snapshots"
        
        # Create directory structure
        for directory in [self.SERVICE_DIR, self.LOGS_DIR, self.SNAPSHOTS_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    def save_service(self, name: str, service_data: Dict[str, Any]) -> bool:
        """Save service data to JSON file."""
        try:
            # Ensure service data has required fields
            service_data.update({
                "name": name,
                "last_updated": datetime.now().isoformat(),
                "registry_version": "1.0"
            })
            
            # Clean name for filename
            clean_name = name.replace(' ', '_').replace('/', '_').lower()
            service_file = self.SERVICE_DIR / f"{clean_name}.json"
            
            with open(service_file, "w") as f:
                json.dump(service_data, f, indent=2)
            
            print(f"📋 Service registered: {name} -> {service_file.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save service {name}: {e}")
            return False
    
    def load_service(self, name: str) -> Optional[Dict[str, Any]]:
        """Load service data from JSON file."""
        try:
            clean_name = name.replace(' ', '_').replace('/', '_').lower()
            service_file = self.SERVICE_DIR / f"{clean_name}.json"
            
            if service_file.exists():
                with open(service_file, "r") as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            print(f"❌ Failed to load service {name}: {e}")
            return None
    
    def list_services(self) -> List[Dict[str, Any]]:
        """List all registered services."""
        services = []
        
        for service_file in self.SERVICE_DIR.glob("*.json"):
            try:
                with open(service_file, "r") as f:
                    service_data = json.load(f)
                    services.append(service_data)
            except Exception as e:
                print(f"⚠️ Error reading {service_file}: {e}")
        
        return services
    
    def delete_service(self, name: str) -> bool:
        """Delete service data."""
        try:
            clean_name = name.replace(' ', '_').replace('/', '_').lower()
            service_file = self.SERVICE_DIR / f"{clean_name}.json"
            
            if service_file.exists():
                service_file.unlink()
                print(f"🗑️ Service deleted: {name}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Failed to delete service {name}: {e}")
            return False
    
    def log_service_event(self, name: str, event: str, details: Dict[str, Any] = None):
        """Log service events with timestamp."""
        try:
            clean_name = name.replace(' ', '_').replace('/', '_').lower()
            log_file = self.LOGS_DIR / f"{clean_name}.log"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "service": name,
                "event": event,
                "details": details or {}
            }
            
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            print(f"❌ Failed to log event for {name}: {e}")
    
    def create_snapshot(self, snapshot_name: str = None) -> str:
        """Create a snapshot of all service data."""
        try:
            if not snapshot_name:
                snapshot_name = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            snapshot_data = {
                "snapshot_name": snapshot_name,
                "created": datetime.now().isoformat(),
                "services": self.list_services()
            }
            
            snapshot_file = self.SNAPSHOTS_DIR / f"{snapshot_name}.json"
            with open(snapshot_file, "w") as f:
                json.dump(snapshot_data, f, indent=2)
            
            print(f"📸 Snapshot created: {snapshot_name}")
            return snapshot_name
            
        except Exception as e:
            print(f"❌ Failed to create snapshot: {e}")
            return None
    
    def restore_from_snapshot(self, snapshot_name: str) -> bool:
        """Restore services from a snapshot."""
        try:
            snapshot_file = self.SNAPSHOTS_DIR / f"{snapshot_name}.json"
            
            if not snapshot_file.exists():
                print(f"❌ Snapshot not found: {snapshot_name}")
                return False
            
            with open(snapshot_file, "r") as f:
                snapshot_data = json.load(f)
            
            restored_count = 0
            for service_data in snapshot_data.get("services", []):
                service_name = service_data.get("name")
                if service_name and self.save_service(service_name, service_data):
                    restored_count += 1
            
            print(f"📁 Restored {restored_count} services from snapshot: {snapshot_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore from snapshot {snapshot_name}: {e}")
            return False
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        services = self.list_services()
        
        stats = {
            "total_services": len(services),
            "active_services": len([s for s in services if s.get("status") == "running"]),
            "stopped_services": len([s for s in services if s.get("status") == "stopped"]),
            "registry_size": sum(f.stat().st_size for f in self.SERVICE_DIR.glob("*.json")),
            "last_updated": max([s.get("last_updated", "") for s in services] or [""]),
            "service_types": {}
        }
        
        # Count service types
        for service in services:
            service_type = service.get("type", "unknown")
            stats["service_types"][service_type] = stats["service_types"].get(service_type, 0) + 1
        
        return stats

# Global registry instance
_registry = None

def get_registry(base_dir: str = None) -> ServiceRegistry:
    """Get or create global service registry instance."""
    global _registry
    if _registry is None:
        _registry = ServiceRegistry(base_dir)
    return _registry

def register_service(name: str, service_data: Dict[str, Any]) -> bool:
    """Convenience function to register a service."""
    registry = get_registry()
    
    # Ensure service directory exists
    SERVICE_DIR = "services/"
    os.makedirs(SERVICE_DIR, exist_ok=True)
    
    # Save using both registry and direct file approach
    registry.save_service(name, service_data)
    
    # Also save directly as requested
    with open(os.path.join(SERVICE_DIR, f"{name}.json"), "w") as f:
        json.dump(service_data, f, indent=2)
    
    return True

if __name__ == "__main__":
    # Test the registry functionality
    registry = ServiceRegistry()
    
    # Test data
    test_service = {
        "command": ["python", "app.py"],
        "status": "running",
        "type": "web_api",
        "port": 5000
    }
    
    # Save service
    registry.save_service("test_api", test_service)
    
    # Load service
    loaded = registry.load_service("test_api")
    print("Loaded service:", loaded)
    
    # List services
    services = registry.list_services()
    print("All services:", services)
    
    # Get stats
    stats = registry.get_service_stats()
    print("Registry stats:", stats)