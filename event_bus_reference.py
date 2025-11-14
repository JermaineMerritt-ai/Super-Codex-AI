#!/usr/bin/env python3
"""
Event Bus Quick Reference
=========================

Simple, fast, and reliable publish-subscribe pattern for Super-Codex-AI.

API:
    bus.on(event_type, handler_function)  # Register handler
    bus.emit(event_type, payload_dict)    # Emit event

Examples:
"""

from codex.core import bus

# =====================================
# BASIC USAGE PATTERNS
# =====================================

# 1. Simple handler registration
def on_user_action(payload):
    print(f"User {payload['user']} performed {payload['action']}")

bus.on('user.action', on_user_action)

# 2. Emit events with data
bus.emit('user.action', {
    'user': 'alice@example.com',
    'action': 'document_upload',
    'filename': 'report.pdf'
})

# =====================================
# ADVANCED PATTERNS
# =====================================

# 3. Multiple handlers for same event
def log_user_action(payload):
    # Log to audit system
    pass

def track_user_action(payload):
    # Update analytics
    pass

bus.on('user.action', log_user_action)
bus.on('user.action', track_user_action)

# 4. Cross-system integration
def on_ai_completion(payload):
    # Trigger follow-up actions
    if payload['operation'] == 'analysis':
        bus.emit('notification.send', {
            'recipient': payload['user'],
            'message': 'Analysis completed',
            'data': payload['results']
        })

bus.on('ai.completion', on_ai_completion)

# 5. Error handling (handlers are called safely)
def safe_handler(payload):
    try:
        # Your logic here
        process_data(payload)
    except Exception as e:
        bus.emit('system.error', {
            'handler': 'safe_handler',
            'error': str(e),
            'payload': payload
        })

bus.on('data.received', safe_handler)

# =====================================
# COMMON EVENT TYPES
# =====================================

# System events
bus.on('system.startup', lambda p: print("System started"))
bus.on('system.shutdown', lambda p: print("System shutting down"))
bus.on('system.error', lambda p: print(f"Error: {p['error']}"))

# User events  
bus.on('user.login', lambda p: print(f"Login: {p['user']}"))
bus.on('user.logout', lambda p: print(f"Logout: {p['user']}"))
bus.on('user.action', lambda p: print(f"Action: {p['action']}"))

# AI events
bus.on('ai.request', lambda p: print(f"AI request: {p['type']}"))
bus.on('ai.completion', lambda p: print(f"AI completed: {p['operation']}"))
bus.on('ai.error', lambda p: print(f"AI error: {p['error']}"))

# Data events
bus.on('data.ingested', lambda p: print(f"Data ingested: {p['records']} records"))
bus.on('data.processed', lambda p: print(f"Data processed: {p['items']} items"))
bus.on('data.exported', lambda p: print(f"Data exported to: {p['destination']}"))

# =====================================
# TESTING UTILITIES
# =====================================

def test_event_system():
    """Test all registered handlers"""
    event_count = 0
    
    def test_handler(payload):
        nonlocal event_count
        event_count += 1
        print(f"Test event {event_count}: {payload}")
    
    # Register test handler for all event types
    for event_type in ['test.basic', 'test.advanced', 'test.integration']:
        bus.on(event_type, test_handler)
    
    # Emit test events
    bus.emit('test.basic', {'status': 'ok'})
    bus.emit('test.advanced', {'features': ['pub', 'sub', 'multi']})
    bus.emit('test.integration', {'systems': ['core', 'api', 'engine']})
    
    print(f"✅ Event system test completed - {event_count} events processed")

if __name__ == "__main__":
    print(__doc__)
    test_event_system()