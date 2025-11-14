#!/usr/bin/env python3
"""Test script for the simplified event bus functionality"""

from codex.core.bus import bus

def main():
    print("🚌 Testing Simplified Event Bus")
    print("-" * 40)
    
    # Define some event handlers
    def handle_user_action(payload):
        print(f"👤 User Action: {payload['action']} by {payload['user']}")
    
    def handle_system_event(payload):
        print(f"⚙️  System Event: {payload['type']} - {payload['message']}")
    
    def handle_ai_event(payload):
        print(f"🤖 AI Event: {payload['operation']} completed")
    
    # Register event handlers
    print("1. Registering event handlers...")
    bus.on('user.action', handle_user_action)
    bus.on('system.event', handle_system_event) 
    bus.on('ai.operation', handle_ai_event)
    
    # Emit various events
    print("\n2. Emitting events...")
    
    # User events
    bus.emit('user.action', {
        'user': 'alice@codex.ai',
        'action': 'login',
        'timestamp': '2025-11-12T10:30:00Z'
    })
    
    bus.emit('user.action', {
        'user': 'bob@codex.ai', 
        'action': 'query',
        'query': 'Show me the latest AI models'
    })
    
    # System events
    bus.emit('system.event', {
        'type': 'startup',
        'message': 'Codex AI system initialized',
        'components': ['core', 'api', 'engine']
    })
    
    bus.emit('system.event', {
        'type': 'health_check',
        'message': 'All systems operational',
        'status': 'healthy'
    })
    
    # AI operation events
    bus.emit('ai.operation', {
        'operation': 'vector_indexing',
        'documents_processed': 1500,
        'duration_ms': 234
    })
    
    bus.emit('ai.operation', {
        'operation': 'model_inference',
        'model': 'codex-v3',
        'tokens_generated': 150
    })
    
    # Test multiple handlers for same event
    print("\n3. Testing multiple handlers for same event...")
    
    def secondary_user_handler(payload):
        print(f"📊 Analytics: Recording {payload['action']} event")
    
    def audit_user_handler(payload):
        print(f"🔍 Audit: User {payload['user']} performed {payload['action']}")
    
    # Register additional handlers for user.action
    bus.on('user.action', secondary_user_handler)
    bus.on('user.action', audit_user_handler)
    
    # Emit a user action that will trigger all three handlers
    bus.emit('user.action', {
        'user': 'charlie@codex.ai',
        'action': 'file_upload',
        'filename': 'document.pdf'
    })
    
    # Test event with no handlers
    print("\n4. Testing event with no handlers...")
    bus.emit('unknown.event', {'data': 'This event has no handlers'})
    print("   ✅ No handlers called (expected behavior)")
    
    print("\n✨ Event bus test completed successfully!")
    print(f"📈 Current handlers registered:")
    for event_type, handlers in bus._handlers.items():
        print(f"   - {event_type}: {len(handlers)} handler(s)")

if __name__ == "__main__":
    main()