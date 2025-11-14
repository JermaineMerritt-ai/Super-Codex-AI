#!/usr/bin/env python3
"""Practical example demonstrating the simplified event bus API"""

from codex.core import bus

def main():
    print("🎯 Simplified Event Bus API Demo")
    print("=" * 40)
    
    # Define handler functions
    def handle_user_login(payload):
        print(f"🔐 User logged in: {payload['username']} from {payload['ip']}")
    
    def handle_api_request(payload):
        print(f"📡 API call: {payload['method']} {payload['endpoint']}")
    
    def handle_system_alert(payload):
        print(f"⚠️  System Alert: {payload['level'].upper()} - {payload['message']}")
    
    def handle_data_processed(payload):
        print(f"📊 Data processed: {payload['records']} records in {payload['time_ms']}ms")
    
    # Register event handlers using the simple API
    print("1. Registering event handlers...")
    bus.on('user.login', handle_user_login)
    bus.on('api.request', handle_api_request)
    bus.on('system.alert', handle_system_alert)
    bus.on('data.processed', handle_data_processed)
    
    print("   ✅ All handlers registered")
    
    # Emit events with payloads
    print("\n2. Emitting events...")
    
    # User login events
    bus.emit('user.login', {
        'username': 'admin@codex.ai',
        'ip': '192.168.1.100',
        'timestamp': '2025-11-12T15:30:00Z'
    })
    
    bus.emit('user.login', {
        'username': 'developer@codex.ai',
        'ip': '10.0.0.50',
        'timestamp': '2025-11-12T15:35:00Z'
    })
    
    # API request events
    bus.emit('api.request', {
        'method': 'POST',
        'endpoint': '/api/v1/generate',
        'user': 'client@company.com'
    })
    
    bus.emit('api.request', {
        'method': 'GET',
        'endpoint': '/api/v1/status',
        'user': 'monitoring@codex.ai'
    })
    
    # System alerts
    bus.emit('system.alert', {
        'level': 'warning',
        'message': 'High memory usage detected',
        'component': 'ai-engine'
    })
    
    bus.emit('system.alert', {
        'level': 'info',
        'message': 'Database backup completed',
        'component': 'postgres'
    })
    
    # Data processing events
    bus.emit('data.processed', {
        'records': 15000,
        'time_ms': 2350,
        'source': 'document_ingestion'
    })
    
    bus.emit('data.processed', {
        'records': 500,
        'time_ms': 120,
        'source': 'vector_indexing'
    })
    
    print("\n3. Demonstrating multiple handlers for same event...")
    
    # Add additional handlers for the same event type
    def audit_user_login(payload):
        print(f"📝 AUDIT: Login recorded for {payload['username']}")
    
    def security_check_login(payload):
        if payload['ip'].startswith('192.168'):
            print(f"🔒 SECURITY: Internal network login - OK")
        else:
            print(f"🚨 SECURITY: External login requires review")
    
    # Register multiple handlers for the same event
    bus.on('user.login', audit_user_login)
    bus.on('user.login', security_check_login)
    
    # Emit a login event that will trigger all three handlers
    bus.emit('user.login', {
        'username': 'external@partner.com',
        'ip': '203.0.113.10',
        'timestamp': '2025-11-12T15:40:00Z'
    })
    
    print("\n4. Event bus state summary:")
    print(f"   📋 Event types registered: {len(bus._handlers)}")
    for event_type, handlers in bus._handlers.items():
        print(f"   - {event_type}: {len(handlers)} handler(s)")
    
    print("\n✨ Event bus demo completed!")

if __name__ == "__main__":
    main()