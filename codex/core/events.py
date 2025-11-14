#!/usr/bin/env python3
"""
Event Management System for Super-Codex-AI
Provides event handling and bus integration
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .bus import bus  # Import the main event bus

class EventType(Enum):
    """Standard event types for the system"""
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown" 
    SYSTEM_ERROR = "system.error"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    USER_ACTION = "user.action"
    AI_REQUEST = "ai.request"
    AI_COMPLETION = "ai.completion"
    AI_ERROR = "ai.error"
    DATA_INGESTED = "data.ingested"
    DATA_PROCESSED = "data.processed"
    DATA_EXPORTED = "data.exported"
    CEREMONY_STARTED = "ceremony.started"
    CEREMONY_COMPLETED = "ceremony.completed"
    ARTIFACT_CREATED = "artifact.created"
    ARTIFACT_DISPATCHED = "artifact.dispatched"
    FORECAST = "forecast"

@dataclass
class Event:
    """Structured event data"""
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    source: Optional[str] = None
    correlation_id: Optional[str] = None

class EventManager:
    """Enhanced event manager with filtering and history"""
    
    def __init__(self):
        self.event_history: List[Event] = []
        self.max_history_size = 1000
        
    def emit_event(self, event_type: str, payload: Dict[str, Any], 
                  source: Optional[str] = None, correlation_id: Optional[str] = None):
        """Emit an event through the bus and record it in history"""
        event = Event(
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(),
            source=source,
            correlation_id=correlation_id
        )
        
        # Add to history (with size limit)
        self.event_history.append(event)
        if len(self.event_history) > self.max_history_size:
            self.event_history.pop(0)
        
        # Emit through bus
        bus.emit(event_type, payload)
        
    def register_handler(self, event_type: str, handler: Callable):
        """Register an event handler"""
        bus.on(event_type, handler)
        
    def get_event_history(self, event_type: Optional[str] = None, 
                         limit: Optional[int] = None) -> List[Event]:
        """Get event history with optional filtering"""
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
            
        if limit:
            events = events[-limit:]
            
        return events
        
    def clear_history(self):
        """Clear event history"""
        self.event_history.clear()

# Global event manager instance
event_manager = EventManager()

# Convenience functions that match the original bus interface
def on(event_type: str, handler: Callable):
    """Register an event handler (convenience function)"""
    event_manager.register_handler(event_type, handler)

def emit(event_type: str, payload: Dict[str, Any], 
         source: Optional[str] = None, correlation_id: Optional[str] = None):
    """Emit an event (convenience function)"""
    event_manager.emit_event(event_type, payload, source, correlation_id)

# Export the bus object for backward compatibility
events_bus = bus

# Standard event emitters for common scenarios
def emit_system_startup():
    """Emit system startup event"""
    emit(EventType.SYSTEM_STARTUP.value, {"message": "System starting up"})

def emit_system_shutdown():
    """Emit system shutdown event"""
    emit(EventType.SYSTEM_SHUTDOWN.value, {"message": "System shutting down"})

def emit_user_action(user: str, action: str, details: Optional[Dict] = None):
    """Emit user action event"""
    payload = {"user": user, "action": action}
    if details:
        payload.update(details)
    emit(EventType.USER_ACTION.value, payload)

def emit_ai_completion(operation: str, user: str, results: Optional[Dict] = None):
    """Emit AI completion event"""
    payload = {"operation": operation, "user": user}
    if results:
        payload["results"] = results
    emit(EventType.AI_COMPLETION.value, payload)

def emit_data_processed(items: int, source: Optional[str] = None):
    """Emit data processed event"""
    emit(EventType.DATA_PROCESSED.value, {"items": items}, source)

def emit_ceremony_event(ceremony_type: str, status: str, details: Optional[Dict] = None):
    """Emit ceremony-related event"""
    event_type = EventType.CEREMONY_STARTED.value if status == "started" else EventType.CEREMONY_COMPLETED.value
    payload = {"ceremony_type": ceremony_type, "status": status}
    if details:
        payload.update(details)
    emit(event_type, payload)

def emit_forecast_event(scenario: str, trend: str, confidence: str = "medium"):
    """Emit forecast event"""
    emit(EventType.FORECAST.value, {
        "scenario": scenario,
        "trend": trend,
        "confidence": confidence
    })

# Testing utilities
def setup_test_handlers():
    """Set up test event handlers for debugging"""
    def log_event(event_type: str):
        def handler(payload):
            print(f"[EVENT] {event_type}: {payload}")
        return handler
    
    # Register handlers for all standard event types
    for event_type in EventType:
        on(event_type.value, log_event(event_type.value))

if __name__ == "__main__":
    # Test the event system
    print("Testing Event Management System...")
    
    setup_test_handlers()
    
    # Test various events
    emit_system_startup()
    emit_user_action("test_user", "document_upload", {"filename": "test.pdf"})
    emit_ai_completion("analysis", "test_user", {"status": "completed"})
    emit_data_processed(100, "import_system")
    emit_ceremony_event("initiation", "started", {"participant": "new_member"})
    emit_forecast_event("market_analysis", "up", "high")
    
    print(f"\nEvent history contains {len(event_manager.event_history)} events")
    
    # Show recent events
    recent_events = event_manager.get_event_history(limit=3)
    print("\nRecent events:")
    for event in recent_events:
        print(f"  {event.timestamp}: {event.event_type} - {event.payload}")