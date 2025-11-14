"""
Codex Audit System
Comprehensive audit trail management with event logging, query tracking,
and integration with the existing ledger system for compliance and debugging.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone, timedelta
import logging
import json
import hashlib
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ledger_system import write_ledger, read_ledger_entries

logger = logging.getLogger(__name__)


class AuditLevel(Enum):
    """Audit detail levels"""
    MINIMAL = "minimal"
    STANDARD = "standard" 
    VERBOSE = "verbose"
    DEBUG = "debug"


class EventType(Enum):
    """Types of auditable events"""
    QUERY = "query"
    INGESTION = "ingestion"
    SYSTEM = "system"
    ERROR = "error"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class AuditEvent:
    """Structured audit event"""
    event_id: str
    event_type: EventType
    action: str
    timestamp: str
    details: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = None
    system_context: Optional[Dict[str, Any]] = None
    severity: str = "info"  # info, warning, error, critical
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        """Create from dictionary"""
        data['event_type'] = EventType(data['event_type'])
        return cls(**data)


class QueryTracker:
    """Track query lifecycle and performance"""
    
    def __init__(self, max_queries: int = 1000):
        self.active_queries: Dict[str, Dict[str, Any]] = {}
        self.completed_queries: deque = deque(maxlen=max_queries)
        self.query_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "errors": 0})
    
    def start_query(self, query_id: str, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start tracking a query"""
        query_info = {
            "query_id": query_id,
            "query": query[:200] + "..." if len(query) > 200 else query,
            "context": context or {},
            "start_time": datetime.now(timezone.utc),
            "events": [],
            "status": "active"
        }
        
        self.active_queries[query_id] = query_info
        return query_info
    
    def add_query_event(self, query_id: str, event_type: str, details: Dict[str, Any]):
        """Add event to query timeline"""
        if query_id in self.active_queries:
            event = {
                "event_type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": details
            }
            self.active_queries[query_id]["events"].append(event)
    
    def complete_query(self, query_id: str, result: str = "success", error: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Complete query tracking"""
        if query_id not in self.active_queries:
            return None
        
        query_info = self.active_queries.pop(query_id)
        query_info["status"] = result
        query_info["end_time"] = datetime.now(timezone.utc)
        query_info["duration"] = (query_info["end_time"] - query_info["start_time"]).total_seconds()
        
        if error:
            query_info["error"] = error
        
        # Update statistics
        query_type = query_info["context"].get("scroll_type", "general")
        stats = self.query_stats[query_type]
        stats["count"] += 1
        stats["total_time"] += query_info["duration"]
        if error:
            stats["errors"] += 1
        
        # Add to completed queries
        self.completed_queries.append(query_info)
        
        return query_info
    
    def get_query_info(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Get query information"""
        # Check active queries
        if query_id in self.active_queries:
            return self.active_queries[query_id]
        
        # Check completed queries
        for query_info in self.completed_queries:
            if query_info["query_id"] == query_id:
                return query_info
        
        return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        total_queries = sum(stats["count"] for stats in self.query_stats.values())
        total_time = sum(stats["total_time"] for stats in self.query_stats.values())
        total_errors = sum(stats["errors"] for stats in self.query_stats.values())
        
        return {
            "total_queries": total_queries,
            "total_processing_time": total_time,
            "average_response_time": total_time / total_queries if total_queries > 0 else 0,
            "error_rate": total_errors / total_queries if total_queries > 0 else 0,
            "active_queries": len(self.active_queries),
            "by_type": dict(self.query_stats),
            "last_hour_queries": self._get_recent_query_count(hours=1),
            "last_day_queries": self._get_recent_query_count(hours=24)
        }
    
    def _get_recent_query_count(self, hours: int) -> int:
        """Count queries in the last N hours"""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        count = 0
        
        for query_info in self.completed_queries:
            if query_info.get("end_time", datetime.min.replace(tzinfo=timezone.utc)) >= cutoff:
                count += 1
        
        return count


class EventBuffer:
    """Buffer for batching audit events"""
    
    def __init__(self, max_size: int = 100, flush_interval: int = 30):
        self.max_size = max_size
        self.flush_interval = flush_interval
        self.buffer: List[AuditEvent] = []
        self.last_flush = datetime.now(timezone.utc)
    
    def add_event(self, event: AuditEvent) -> bool:
        """Add event to buffer, return True if flush is needed"""
        self.buffer.append(event)
        
        # Check if flush is needed
        now = datetime.now(timezone.utc)
        return (
            len(self.buffer) >= self.max_size or
            (now - self.last_flush).total_seconds() >= self.flush_interval
        )
    
    def get_events(self) -> List[AuditEvent]:
        """Get and clear buffered events"""
        events = self.buffer.copy()
        self.buffer.clear()
        self.last_flush = datetime.now(timezone.utc)
        return events
    
    def is_empty(self) -> bool:
        """Check if buffer is empty"""
        return len(self.buffer) == 0


class CodexAuditor:
    """Main audit system for Codex"""
    
    def __init__(self, config):
        self.config = config
        self.audit_level = AuditLevel(config.audit_detail_level)
        self.enabled = config.audit_enabled
        self.ledger_integration = config.ledger_integration
        
        # Components
        self.query_tracker = QueryTracker()
        self.event_buffer = EventBuffer()
        self.session_events: Dict[str, List[AuditEvent]] = {}
        
        # Performance tracking
        self.performance_metrics = defaultdict(list)
        self.error_patterns = defaultdict(int)
        
        # Background task for flushing
        self._flush_task = None
    
    async def initialize(self):
        """Initialize the audit system"""
        if not self.enabled:
            logger.info("Audit system disabled by configuration")
            return
        
        # Start background flush task
        self._flush_task = asyncio.create_task(self._flush_loop())
        
        # Log initialization
        await self.log_event({
            "action": "audit_system_initialized",
            "audit_level": self.audit_level.value,
            "ledger_integration": self.ledger_integration,
            "configuration": {
                "retention_days": self.config.audit_retention_days,
                "detail_level": self.audit_level.value
            }
        }, EventType.SYSTEM)
        
        logger.info(f"Audit system initialized with {self.audit_level.value} detail level")
    
    async def shutdown(self):
        """Shutdown the audit system"""
        if not self.enabled:
            return
        
        # Cancel flush task
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
        
        # Final flush
        await self._flush_events()
        
        logger.info("Audit system shutdown complete")
    
    async def log_event(self, details: Dict[str, Any], event_type: EventType = EventType.SYSTEM,
                       severity: str = "info", session_id: Optional[str] = None,
                       correlation_id: Optional[str] = None) -> str:
        """Log an audit event"""
        if not self.enabled:
            return ""
        
        # Generate event ID
        event_id = self._generate_event_id(details)
        
        # Create audit event
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            action=details.get("action", "unknown"),
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=details,
            severity=severity,
            session_id=session_id,
            correlation_id=correlation_id,
            system_context=self._get_system_context(),
            user_context=self._get_user_context()
        )
        
        # Add to session tracking
        if session_id:
            if session_id not in self.session_events:
                self.session_events[session_id] = []
            self.session_events[session_id].append(event)
        
        # Track performance metrics
        if event_type == EventType.PERFORMANCE:
            self._track_performance_metric(details)
        
        # Track error patterns
        if event_type == EventType.ERROR:
            self._track_error_pattern(details)
        
        # Add to buffer
        if self.event_buffer.add_event(event):
            await self._flush_events()
        
        return event_id
    
    async def start_query_audit(self, query_id: str, query: str, context: Dict[str, Any] = None) -> str:
        """Start auditing a query"""
        # Start tracking
        self.query_tracker.start_query(query_id, query, context)
        
        # Log event
        return await self.log_event({
            "action": "query_started",
            "query_id": query_id,
            "query_preview": query[:100] + "..." if len(query) > 100 else query,
            "context": context or {},
            "scroll_type": context.get("scroll_type") if context else None
        }, EventType.QUERY, correlation_id=query_id)
    
    async def add_query_step(self, query_id: str, step: str, details: Dict[str, Any]):
        """Add a step to query audit trail"""
        self.query_tracker.add_query_event(query_id, step, details)
        
        if self.audit_level in [AuditLevel.VERBOSE, AuditLevel.DEBUG]:
            await self.log_event({
                "action": f"query_{step}",
                "query_id": query_id,
                "step_details": details
            }, EventType.QUERY, correlation_id=query_id)
    
    async def complete_query_audit(self, query_id: str, success: bool = True, 
                                  error: Optional[str] = None, 
                                  performance_data: Optional[Dict[str, Any]] = None):
        """Complete query audit"""
        # Complete tracking
        query_info = self.query_tracker.complete_query(
            query_id, 
            "success" if success else "error", 
            error
        )
        
        # Log completion
        await self.log_event({
            "action": "query_completed",
            "query_id": query_id,
            "success": success,
            "error": error,
            "duration": query_info.get("duration") if query_info else None,
            "performance": performance_data
        }, EventType.QUERY if success else EventType.ERROR, 
        severity="info" if success else "error",
        correlation_id=query_id)
    
    async def audit_ingestion(self, file_path: str, result: Dict[str, Any], 
                             success: bool = True, error: Optional[str] = None):
        """Audit document ingestion"""
        await self.log_event({
            "action": "document_ingestion",
            "file_path": file_path,
            "success": success,
            "error": error,
            "chunks_created": result.get("chunks_created", 0),
            "vectors_indexed": result.get("vectors_indexed", 0),
            "document_type": result.get("document_type"),
            "content_type": result.get("content_type")
        }, EventType.INGESTION if success else EventType.ERROR,
        severity="info" if success else "error")
    
    async def audit_security_event(self, event_type: str, details: Dict[str, Any], severity: str = "warning"):
        """Audit security-related events"""
        await self.log_event({
            "action": f"security_{event_type}",
            **details
        }, EventType.SECURITY, severity=severity)
    
    async def get_query_trail(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Get complete audit trail for a query"""
        query_info = self.query_tracker.get_query_info(query_id)
        
        if not query_info:
            return None
        
        # Get related audit events from ledger if enabled
        related_events = []
        if self.ledger_integration:
            try:
                all_events = read_ledger_entries("codex_audit")
                related_events = [
                    event for event in all_events 
                    if event.get("correlation_id") == query_id
                ]
            except Exception as e:
                logger.warning(f"Failed to read audit ledger: {e}")
        
        return {
            "query_info": query_info,
            "audit_events": related_events,
            "performance_summary": self._get_query_performance_summary(query_id)
        }
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get performance dashboard data"""
        query_stats = self.query_tracker.get_performance_stats()
        
        return {
            "queries": query_stats,
            "top_error_patterns": dict(sorted(self.error_patterns.items(), 
                                             key=lambda x: x[1], reverse=True)[:10]),
            "recent_performance": self._get_recent_performance_summary(),
            "system_health": self._assess_system_health()
        }
    
    def _generate_event_id(self, details: Dict[str, Any]) -> str:
        """Generate unique event ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        content_hash = hashlib.md5(json.dumps(details, sort_keys=True).encode()).hexdigest()[:8]
        return f"evt_{timestamp}_{content_hash}"
    
    def _get_system_context(self) -> Dict[str, Any]:
        """Get current system context"""
        return {
            "audit_level": self.audit_level.value,
            "active_queries": len(self.query_tracker.active_queries),
            "buffer_size": len(self.event_buffer.buffer)
        }
    
    def _get_user_context(self) -> Optional[Dict[str, Any]]:
        """Get user context (placeholder for future authentication integration)"""
        # In production, this would extract user info from request context
        return None
    
    def _track_performance_metric(self, details: Dict[str, Any]):
        """Track performance metrics"""
        metric_name = details.get("metric", "unknown")
        value = details.get("value", 0)
        
        self.performance_metrics[metric_name].append({
            "timestamp": datetime.now(timezone.utc),
            "value": value
        })
        
        # Keep only recent metrics (last 1000 per metric)
        if len(self.performance_metrics[metric_name]) > 1000:
            self.performance_metrics[metric_name] = self.performance_metrics[metric_name][-1000:]
    
    def _track_error_pattern(self, details: Dict[str, Any]):
        """Track error patterns for analysis"""
        error_type = details.get("error_type", "unknown")
        self.error_patterns[error_type] += 1
    
    def _get_query_performance_summary(self, query_id: str) -> Dict[str, Any]:
        """Get performance summary for a specific query"""
        query_info = self.query_tracker.get_query_info(query_id)
        
        if not query_info:
            return {}
        
        return {
            "duration": query_info.get("duration"),
            "events_count": len(query_info.get("events", [])),
            "status": query_info.get("status"),
            "timeline": query_info.get("events", [])
        }
    
    def _get_recent_performance_summary(self) -> Dict[str, Any]:
        """Get summary of recent performance metrics"""
        summary = {}
        
        for metric_name, values in self.performance_metrics.items():
            if values:
                recent_values = [v["value"] for v in values[-100:]]  # Last 100 values
                summary[metric_name] = {
                    "average": sum(recent_values) / len(recent_values),
                    "min": min(recent_values),
                    "max": max(recent_values),
                    "count": len(recent_values)
                }
        
        return summary
    
    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health based on audit data"""
        stats = self.query_tracker.get_performance_stats()
        
        # Simple health assessment
        health_score = 100
        issues = []
        
        # Check error rate
        error_rate = stats.get("error_rate", 0)
        if error_rate > 0.1:  # > 10% error rate
            health_score -= 30
            issues.append(f"High error rate: {error_rate:.1%}")
        
        # Check response time
        avg_response = stats.get("average_response_time", 0)
        if avg_response > 5.0:  # > 5 seconds average
            health_score -= 20
            issues.append(f"Slow response time: {avg_response:.1f}s")
        
        # Check active queries
        active_queries = stats.get("active_queries", 0)
        if active_queries > 50:  # Too many concurrent queries
            health_score -= 15
            issues.append(f"High concurrent load: {active_queries} active queries")
        
        # Determine health status
        if health_score >= 80:
            status = "healthy"
        elif health_score >= 60:
            status = "degraded"
        elif health_score >= 40:
            status = "unhealthy"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": max(0, health_score),
            "issues": issues,
            "recommendations": self._get_health_recommendations(issues)
        }
    
    def _get_health_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations based on health issues"""
        recommendations = []
        
        for issue in issues:
            if "error rate" in issue:
                recommendations.append("Review error logs and fix common failure patterns")
            elif "response time" in issue:
                recommendations.append("Optimize query processing and consider scaling resources")
            elif "concurrent load" in issue:
                recommendations.append("Implement query throttling or increase processing capacity")
        
        return recommendations
    
    async def _flush_events(self):
        """Flush buffered events to ledger"""
        if not self.ledger_integration or self.event_buffer.is_empty():
            return
        
        try:
            events = self.event_buffer.get_events()
            
            for event in events:
                write_ledger("codex_audit", event.to_dict())
            
            logger.debug(f"Flushed {len(events)} audit events to ledger")
            
        except Exception as e:
            logger.error(f"Failed to flush audit events: {e}")
    
    async def _flush_loop(self):
        """Background task for periodic event flushing"""
        try:
            while True:
                await asyncio.sleep(30)  # Flush every 30 seconds
                await self._flush_events()
        except asyncio.CancelledError:
            logger.debug("Audit flush loop cancelled")
            raise
        except Exception as e:
            logger.error(f"Audit flush loop error: {e}")


# Example usage
if __name__ == "__main__":
    async def test_audit():
        from config import CodexConfig
        
        config = CodexConfig()
        auditor = CodexAuditor(config)
        
        await auditor.initialize()
        
        # Test query audit
        query_id = "test_query_001"
        await auditor.start_query_audit(query_id, "What is the honor system?", {"scroll_type": "general"})
        await auditor.add_query_step(query_id, "embedding_generated", {"dimension": 1536})
        await auditor.add_query_step(query_id, "similarity_search", {"results_found": 3})
        await auditor.complete_query_audit(query_id, success=True, performance_data={"response_time": 1.2})
        
        # Test performance dashboard
        dashboard = auditor.get_performance_dashboard()
        print(f"Performance Dashboard: {dashboard}")
        
        await auditor.shutdown()
    
    asyncio.run(test_audit())