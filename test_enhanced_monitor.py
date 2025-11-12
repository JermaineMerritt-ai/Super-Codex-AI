#!/usr/bin/env python3
"""
Test Enhanced Service Monitor with JSON Storage
"""

import time
import sys
import os

# Add current directory to path to import service modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service_monitor import ServiceMonitor
from service_registry import register_service, get_registry

def test_service_with_registry():
    """Test service monitoring with registry integration."""
    
    print("🧪 Testing Enhanced Service Monitor with JSON Storage")
    print("=" * 60)
    
    # Create a service monitor
    monitor = ServiceMonitor("Test Web Service", restart_delay=1)
    
    # Register the service with additional metadata
    service_data = {
        "type": "test_service",
        "description": "Test service for monitor validation",
        "port": 3000,
        "auto_restart": True,
        "environment": {"NODE_ENV": "test"},
        "command": ["python", "test_service.py"]
    }
    
    print("📋 Registering service with registry...")
    register_service("test_web_service", service_data)
    
    # Start monitoring
    print("🔥 Starting service monitor...")
    monitor.start(["python", "test_service.py"])
    
    # Let it run for a few cycles
    print("⏳ Monitoring for 10 seconds...")
    time.sleep(10)
    
    # Stop monitoring
    print("🛑 Stopping service monitor...")
    monitor.stop()
    
    # Check registry stats
    print("\n📊 Registry Statistics:")
    registry = get_registry()
    stats = registry.get_service_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # List all services
    print("\n📋 All Registered Services:")
    services = registry.list_services()
    for service in services:
        print(f"  - {service.get('name', 'Unknown')}: {service.get('status', 'N/A')}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_service_with_registry()