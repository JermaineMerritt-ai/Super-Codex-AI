"""
Codex Real-time Scroll Operations
Real-time scroll generation, streaming, and live updates using WebSocket connections.
Supports collaborative scroll editing and live ceremonial events.
"""

import os
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Callable
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
from collections import defaultdict, deque

# WebSocket and async support
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed, WebSocketException

# Import scroll system components
from .capsule import CapsuleRegistry, ScrollGenerator, CeremonialContext

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of real-time events"""
    SCROLL_REQUEST = "scroll_request"
    SCROLL_PROGRESS = "scroll_progress"
    SCROLL_COMPLETE = "scroll_complete"
    SCROLL_ERROR = "scroll_error"
    CEREMONY_START = "ceremony_start"
    CEREMONY_UPDATE = "ceremony_update"
    CEREMONY_COMPLETE = "ceremony_complete"
    CONNECTION_STATUS = "connection_status"
    SYSTEM_STATUS = "system_status"
    USER_JOIN = "user_join"
    USER_LEAVE = "user_leave"


class ConnectionState(Enum):
    """WebSocket connection states"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class RealtimeEvent:
    """Real-time event structure"""
    event_type: EventType
    event_id: str
    timestamp: str
    data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    target_users: Optional[List[str]] = None
    
    def to_json(self) -> str:
        """Convert to JSON for WebSocket transmission"""
        return json.dumps({
            "event_type": self.event_type.value,
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "user_id": self.user_id,
            "session_id": self.session_id
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> "RealtimeEvent":
        """Create from JSON"""
        data = json.loads(json_str)
        data["event_type"] = EventType(data["event_type"])
        return cls(**data)


@dataclass
class UserConnection:
    """User connection information"""
    user_id: str
    session_id: str
    websocket: WebSocketServerProtocol
    state: ConnectionState
    connected_at: datetime
    last_activity: datetime
    subscriptions: Set[str] = field(default_factory=set)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_alive(self) -> bool:
        """Check if connection is alive"""
        return self.websocket.open and self.state in [ConnectionState.CONNECTED, ConnectionState.AUTHENTICATED]
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now(timezone.utc)


class ScrollSession:
    """Manages a scroll generation session"""
    
    def __init__(self, session_id: str, request_data: Dict[str, Any]):
        self.session_id = session_id
        self.request_data = request_data
        self.created_at = datetime.now(timezone.utc)
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.status = "pending"
        self.progress = 0
        self.current_stage = "initializing"
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
        self.subscribers: Set[str] = set()  # User IDs subscribed to updates
    
    def start(self):
        """Mark session as started"""
        self.started_at = datetime.now(timezone.utc)
        self.status = "processing"
    
    def update_progress(self, progress: int, stage: str):
        """Update progress and stage"""
        self.progress = max(0, min(100, progress))
        self.current_stage = stage
    
    def complete(self, result: Dict[str, Any]):
        """Mark session as completed"""
        self.completed_at = datetime.now(timezone.utc)
        self.status = "completed"
        self.progress = 100
        self.current_stage = "complete"
        self.result = result
    
    def error_out(self, error: str):
        """Mark session as failed"""
        self.completed_at = datetime.now(timezone.utc)
        self.status = "error"
        self.current_stage = "error"
        self.error = error
    
    def add_subscriber(self, user_id: str):
        """Add user subscription to session updates"""
        self.subscribers.add(user_id)
    
    def remove_subscriber(self, user_id: str):
        """Remove user subscription"""
        self.subscribers.discard(user_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current session status"""
        return {
            "session_id": self.session_id,
            "status": self.status,
            "progress": self.progress,
            "current_stage": self.current_stage,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "subscriber_count": len(self.subscribers)
        }


class RealtimeScrollManager:
    """Manages real-time scroll operations and WebSocket connections"""
    
    def __init__(self, config, scroll_generator: ScrollGenerator, 
                 capsule_registry: CapsuleRegistry):
        self.config = config
        self.scroll_generator = scroll_generator
        self.capsule_registry = capsule_registry
        
        # Connection management
        self.connections: Dict[str, UserConnection] = {}  # user_id -> connection
        self.session_connections: Dict[str, Set[str]] = defaultdict(set)  # session_id -> user_ids
        
        # Session management
        self.scroll_sessions: Dict[str, ScrollSession] = {}  # session_id -> session
        
        # Event system
        self.event_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self.event_history: deque = deque(maxlen=1000)  # Keep recent events
        
        # Performance tracking
        self.connection_metrics = {
            "total_connections": 0,
            "active_connections": 0,
            "total_sessions": 0,
            "active_sessions": 0,
            "events_processed": 0
        }
        
        # Background tasks
        self._cleanup_task = None
        self._heartbeat_task = None
    
    async def initialize(self):
        """Initialize the real-time manager"""
        # Start background tasks
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        logger.info("Real-time scroll manager initialized")
    
    async def shutdown(self):
        """Shutdown the real-time manager"""
        # Cancel background tasks
        if self._cleanup_task:
            self._cleanup_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        
        # Close all connections
        for connection in list(self.connections.values()):
            await self.disconnect_user(connection.user_id)
        
        logger.info("Real-time scroll manager shutdown")
    
    async def connect_user(self, user_id: str, websocket: WebSocketServerProtocol,
                          context: Dict[str, Any] = None) -> str:
        """Connect a user with WebSocket"""
        try:
            session_id = str(uuid.uuid4())
            
            # Create connection
            connection = UserConnection(
                user_id=user_id,
                session_id=session_id,
                websocket=websocket,
                state=ConnectionState.CONNECTED,
                connected_at=datetime.now(timezone.utc),
                last_activity=datetime.now(timezone.utc),
                context=context or {}
            )
            
            # Store connection
            self.connections[user_id] = connection
            
            # Update metrics
            self.connection_metrics["total_connections"] += 1
            self.connection_metrics["active_connections"] += 1
            
            # Send welcome event
            welcome_event = RealtimeEvent(
                event_type=EventType.CONNECTION_STATUS,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data={
                    "status": "connected",
                    "session_id": session_id,
                    "message": "Connected to Super-Codex-AI real-time scroll system"
                },
                user_id=user_id,
                session_id=session_id
            )
            
            await self._send_to_user(user_id, welcome_event)
            
            # Broadcast user join
            await self._broadcast_event(RealtimeEvent(
                event_type=EventType.USER_JOIN,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data={"user_id": user_id}
            ))
            
            logger.info(f"User {user_id} connected with session {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to connect user {user_id}: {e}")
            raise
    
    async def disconnect_user(self, user_id: str):
        """Disconnect a user"""
        try:
            connection = self.connections.get(user_id)
            if not connection:
                return
            
            # Close WebSocket
            if connection.is_alive():
                await connection.websocket.close()
            
            # Remove from all session subscriptions
            for session_id in list(self.session_connections.keys()):
                self.session_connections[session_id].discard(user_id)
                if session_id in self.scroll_sessions:
                    self.scroll_sessions[session_id].remove_subscriber(user_id)
            
            # Remove connection
            del self.connections[user_id]
            
            # Update metrics
            self.connection_metrics["active_connections"] -= 1
            
            # Broadcast user leave
            await self._broadcast_event(RealtimeEvent(
                event_type=EventType.USER_LEAVE,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data={"user_id": user_id}
            ))
            
            logger.info(f"User {user_id} disconnected")
            
        except Exception as e:
            logger.error(f"Error disconnecting user {user_id}: {e}")
    
    async def start_scroll_generation(self, request_data: Dict[str, Any],
                                    requesting_user: str) -> str:
        """Start real-time scroll generation"""
        try:
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            # Create session
            session = ScrollSession(session_id, request_data)
            session.add_subscriber(requesting_user)
            self.scroll_sessions[session_id] = session
            
            # Add to session connections
            self.session_connections[session_id].add(requesting_user)
            
            # Update metrics
            self.connection_metrics["total_sessions"] += 1
            self.connection_metrics["active_sessions"] += 1
            
            # Start generation in background
            asyncio.create_task(self._process_scroll_generation(session))
            
            # Send initial event
            start_event = RealtimeEvent(
                event_type=EventType.SCROLL_REQUEST,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data={
                    "session_id": session_id,
                    "status": "started",
                    "query": request_data.get("query", "Unknown"),
                    "capsule_id": request_data.get("capsule_id", "Unknown")
                },
                user_id=requesting_user,
                session_id=session_id
            )
            
            await self._send_to_session_subscribers(session_id, start_event)
            
            logger.info(f"Started scroll generation session {session_id} for user {requesting_user}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start scroll generation: {e}")
            raise
    
    async def subscribe_to_session(self, session_id: str, user_id: str):
        """Subscribe user to session updates"""
        if session_id in self.scroll_sessions:
            self.scroll_sessions[session_id].add_subscriber(user_id)
            self.session_connections[session_id].add(user_id)
            
            # Send current status
            status_event = RealtimeEvent(
                event_type=EventType.SCROLL_PROGRESS,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data=self.scroll_sessions[session_id].get_status(),
                user_id=user_id,
                session_id=session_id
            )
            
            await self._send_to_user(user_id, status_event)
            logger.info(f"User {user_id} subscribed to session {session_id}")
    
    async def unsubscribe_from_session(self, session_id: str, user_id: str):
        """Unsubscribe user from session updates"""
        if session_id in self.scroll_sessions:
            self.scroll_sessions[session_id].remove_subscriber(user_id)
            self.session_connections[session_id].discard(user_id)
            logger.info(f"User {user_id} unsubscribed from session {session_id}")
    
    async def _process_scroll_generation(self, session: ScrollSession):
        """Process scroll generation with progress updates"""
        try:
            session.start()
            
            # Extract request data
            capsule_id = session.request_data.get("capsule_id")
            query = session.request_data.get("query")
            sources = session.request_data.get("sources", [])
            rag_result = session.request_data.get("rag_result", {})
            user_context = session.request_data.get("user_context", {})
            ceremonial_context_data = session.request_data.get("ceremonial_context")
            
            # Build ceremonial context
            ceremonial_context = None
            if ceremonial_context_data:
                ceremonial_context = CeremonialContext(**ceremonial_context_data)
            
            # Progress: Start generation
            session.update_progress(10, "Initializing scroll generation")
            await self._send_progress_update(session)
            
            # Progress: Validate capsule
            session.update_progress(20, "Validating capsule access")
            await self._send_progress_update(session)
            
            # Progress: Prepare context
            session.update_progress(40, "Preparing ceremonial context")
            await self._send_progress_update(session)
            
            # Progress: Generate scroll
            session.update_progress(60, "Generating scroll content")
            await self._send_progress_update(session)
            
            # Perform actual generation
            result = await self.scroll_generator.generate_scroll(
                capsule_id=capsule_id,
                query=query,
                sources=sources,
                rag_result=rag_result,
                user_context=user_context,
                ceremonial_context=ceremonial_context
            )
            
            # Progress: Finalize
            session.update_progress(90, "Finalizing scroll")
            await self._send_progress_update(session)
            
            if result.get("success"):
                session.complete(result)
                
                # Send completion event
                complete_event = RealtimeEvent(
                    event_type=EventType.SCROLL_COMPLETE,
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    data={
                        "session_id": session.session_id,
                        "scroll_content": result["scroll_content"],
                        "scroll_metadata": result["scroll_metadata"],
                        "generation_time": result["scroll_metadata"].get("generation_time")
                    },
                    session_id=session.session_id
                )
                
                await self._send_to_session_subscribers(session.session_id, complete_event)
                
            else:
                session.error_out(result.get("error", "Unknown error"))
                
                # Send error event
                error_event = RealtimeEvent(
                    event_type=EventType.SCROLL_ERROR,
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    data={
                        "session_id": session.session_id,
                        "error": session.error
                    },
                    session_id=session.session_id
                )
                
                await self._send_to_session_subscribers(session.session_id, error_event)
            
            # Update metrics
            self.connection_metrics["active_sessions"] -= 1
            
        except Exception as e:
            logger.error(f"Error in scroll generation session {session.session_id}: {e}")
            session.error_out(str(e))
            
            error_event = RealtimeEvent(
                event_type=EventType.SCROLL_ERROR,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                data={
                    "session_id": session.session_id,
                    "error": str(e)
                },
                session_id=session.session_id
            )
            
            await self._send_to_session_subscribers(session.session_id, error_event)
    
    async def _send_progress_update(self, session: ScrollSession):
        """Send progress update to session subscribers"""
        progress_event = RealtimeEvent(
            event_type=EventType.SCROLL_PROGRESS,
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=session.get_status(),
            session_id=session.session_id
        )
        
        await self._send_to_session_subscribers(session.session_id, progress_event)
    
    async def _send_to_user(self, user_id: str, event: RealtimeEvent):
        """Send event to specific user"""
        connection = self.connections.get(user_id)
        if connection and connection.is_alive():
            try:
                await connection.websocket.send(event.to_json())
                connection.update_activity()
                
            except (ConnectionClosed, WebSocketException) as e:
                logger.warning(f"Failed to send to user {user_id}: {e}")
                await self.disconnect_user(user_id)
    
    async def _send_to_session_subscribers(self, session_id: str, event: RealtimeEvent):
        """Send event to all session subscribers"""
        session = self.scroll_sessions.get(session_id)
        if session:
            tasks = []
            for user_id in session.subscribers:
                tasks.append(self._send_to_user(user_id, event))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _broadcast_event(self, event: RealtimeEvent):
        """Broadcast event to all connected users"""
        if not self.connections:
            return
        
        tasks = []
        for user_id in list(self.connections.keys()):
            tasks.append(self._send_to_user(user_id, event))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _cleanup_loop(self):
        """Background cleanup of stale connections and sessions"""
        try:
            while True:
                await asyncio.sleep(60)  # Run every minute
                
                # Clean up stale connections
                stale_cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
                stale_users = [
                    user_id for user_id, conn in self.connections.items()
                    if conn.last_activity < stale_cutoff or not conn.is_alive()
                ]
                
                for user_id in stale_users:
                    await self.disconnect_user(user_id)
                
                # Clean up old sessions
                old_sessions = [
                    session_id for session_id, session in self.scroll_sessions.items()
                    if session.status in ["completed", "error"] and 
                       session.completed_at and 
                       session.completed_at < datetime.now(timezone.utc) - timedelta(hours=1)
                ]
                
                for session_id in old_sessions:
                    del self.scroll_sessions[session_id]
                    if session_id in self.session_connections:
                        del self.session_connections[session_id]
                
                if stale_users or old_sessions:
                    logger.debug(f"Cleaned up {len(stale_users)} stale connections and {len(old_sessions)} old sessions")
                
        except asyncio.CancelledError:
            logger.debug("Cleanup loop cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in cleanup loop: {e}")
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeat to maintain connections"""
        try:
            while True:
                await asyncio.sleep(30)  # Send every 30 seconds
                
                heartbeat_event = RealtimeEvent(
                    event_type=EventType.SYSTEM_STATUS,
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    data={
                        "status": "online",
                        "active_connections": len(self.connections),
                        "active_sessions": len([s for s in self.scroll_sessions.values() if s.status == "processing"])
                    }
                )
                
                await self._broadcast_event(heartbeat_event)
                
        except asyncio.CancelledError:
            logger.debug("Heartbeat loop cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in heartbeat loop: {e}")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        active_sessions = len([s for s in self.scroll_sessions.values() if s.status == "processing"])
        
        return {
            "active_connections": len(self.connections),
            "total_connections": self.connection_metrics["total_connections"],
            "active_sessions": active_sessions,
            "total_sessions": self.connection_metrics["total_sessions"],
            "events_processed": self.connection_metrics["events_processed"],
            "connected_users": list(self.connections.keys())
        }


# Example usage
if __name__ == "__main__":
    async def test_realtime_system():
        from engine.config import CodexConfig
        from engine.models.prompts import PromptManager
        from capsule import CapsuleRegistry, ScrollGenerator
        
        config = CodexConfig()
        registry = CapsuleRegistry(config)
        prompt_manager = PromptManager(config)
        generator = ScrollGenerator(config, registry, prompt_manager)
        
        manager = RealtimeScrollManager(config, generator, registry)
        await manager.initialize()
        
        print(f"Real-time manager initialized")
        print(f"Connection status: {manager.get_connection_status()}")
        
        await manager.shutdown()
    
    asyncio.run(test_realtime_system())