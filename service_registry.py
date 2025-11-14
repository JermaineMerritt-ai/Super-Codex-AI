"""
Missing service registry module for enhanced monitoring
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Global service registry
_service_registry: Dict[str, Dict[str, Any]] = {}

def register_service(service_id: str, service_data: Dict[str, Any]):
    """Register a service in the global registry"""
    service_data['registered_at'] = datetime.now().isoformat()
    _service_registry[service_id] = service_data

def get_registry() -> Dict[str, Dict[str, Any]]:
    """Get the complete service registry"""
    return _service_registry.copy()

def get_service(service_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific service from the registry"""
    return _service_registry.get(service_id)

def unregister_service(service_id: str) -> bool:
    """Remove a service from the registry"""
    if service_id in _service_registry:
        del _service_registry[service_id]
        return True
    return False

def list_services(service_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all services, optionally filtered by type"""
    services = list(_service_registry.values())
    if service_type:
        services = [s for s in services if s.get('type') == service_type]
    return services

def update_service_status(service_id: str, status: str, additional_data: Optional[Dict[str, Any]] = None):
    """Update service status and optional additional data"""
    if service_id in _service_registry:
        _service_registry[service_id]['status'] = status
        _service_registry[service_id]['last_updated'] = datetime.now().isoformat()
        if additional_data:
            _service_registry[service_id].update(additional_data)