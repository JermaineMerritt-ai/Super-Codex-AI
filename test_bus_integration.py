#!/usr/bin/env python3
"""Integration example showing event bus usage across core components"""

from codex.core import bus, log_event, archive

def main():
    print("🔗 Event Bus Integration Example")
    print("=" * 45)
    
    # Setup cross-system event handlers
    def on_user_activity(payload):
        """Log and archive user activities"""
        # Log the activity for monitoring
        log_event('user_activity', {
            'user': payload['user'],
            'action': payload['action'],
            'source': 'event_bus'
        })
        
        # Archive for long-term storage
        archive(f"user-activity-{payload['action']}", payload)
        print(f"✅ Processed user activity: {payload['action']}")
    
    def on_system_error(payload):
        """Handle system errors with logging and alerts"""
        log_event('system_error', {
            'error': payload['error'],
            'severity': payload.get('severity', 'medium'),
            'component': payload['component']
        })
        
        archive('system-error', payload)
        print(f"🚨 System error processed: {payload['error']}")
    
    def on_ai_completion(payload):
        """Track AI operations and performance"""
        log_event('ai_completion', {
            'operation': payload['operation'],
            'duration': payload.get('duration_ms', 0),
            'status': 'completed'
        })
        
        archive('ai-completion', payload)
        print(f"🤖 AI operation tracked: {payload['operation']}")
    
    # Register handlers
    print("1. Setting up cross-system event handlers...")
    bus.on('user.activity', on_user_activity)
    bus.on('system.error', on_system_error)
    bus.on('ai.completion', on_ai_completion)
    
    # Simulate various system events
    print("\n2. Simulating system events...")
    
    # User activities
    bus.emit('user.activity', {
        'user': 'admin@codex.ai',
        'action': 'dashboard_access',
        'timestamp': '2025-11-12T14:25:00Z',
        'ip': '192.168.1.100'
    })
    
    bus.emit('user.activity', {
        'user': 'developer@codex.ai', 
        'action': 'api_call',
        'endpoint': '/api/v1/generate',
        'method': 'POST'
    })
    
    # System errors
    bus.emit('system.error', {
        'error': 'Database connection timeout',
        'component': 'postgres_connector',
        'severity': 'high',
        'retry_count': 3
    })
    
    bus.emit('system.error', {
        'error': 'Rate limit exceeded',
        'component': 'api_gateway', 
        'severity': 'low',
        'user': 'heavy_user@client.com'
    })
    
    # AI completions
    bus.emit('ai.completion', {
        'operation': 'text_generation',
        'model': 'codex-gpt',
        'duration_ms': 1250,
        'tokens': 500,
        'quality_score': 0.92
    })
    
    bus.emit('ai.completion', {
        'operation': 'code_analysis',
        'model': 'codex-analyzer',
        'duration_ms': 850,
        'files_analyzed': 15,
        'issues_found': 3
    })
    
    print("\n3. Event processing summary:")
    print(f"   📋 Total event types: {len(bus._handlers)}")
    for event_type, handlers in bus._handlers.items():
        print(f"   - {event_type}: {len(handlers)} handler(s)")
    
    print("\n✨ Integration test completed!")
    print("💾 Check ./data/audit/ for logged events")
    print("📁 Check ./data/replay/ for archived data")

if __name__ == "__main__":
    main()