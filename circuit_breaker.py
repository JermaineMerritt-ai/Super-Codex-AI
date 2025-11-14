#!/usr/bin/env python3
"""
Circuit Breaker Pattern Implementation for Health Checks
Prevents cascading failures by stopping requests to failing services
"""
import time
import asyncio
from enum import Enum
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service has recovered

class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        reset_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        async with self._lock:
            if self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitBreakerState.HALF_OPEN
                    logger.info(f"Circuit breaker {self.name} moved to HALF_OPEN")
                else:
                    raise Exception(f"Circuit breaker {self.name} is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                await self._on_success()
                return result
            except self.expected_exception as e:
                await self._on_failure()
                raise e
    
    async def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
            logger.info(f"Circuit breaker {self.name} moved to CLOSED")
    
    async def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
            logger.warning(f"Circuit breaker {self.name} moved to OPEN after {self.failure_count} failures")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = datetime.utcnow() - self.last_failure_time
        return time_since_failure.total_seconds() > self.reset_timeout
    
    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "reset_timeout": self.reset_timeout
        }

class CircuitBreakerRegistry:
    """Global registry for circuit breakers"""
    def __init__(self):
        self._breakers: Dict[str, CircuitBreaker] = {}
    
    def get_or_create(self, name: str, **kwargs) -> CircuitBreaker:
        """Get existing circuit breaker or create new one"""
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name=name, **kwargs)
        return self._breakers[name]
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all circuit breakers"""
        return {name: breaker.get_status() for name, breaker in self._breakers.items()}

# Global registry instance
circuit_breaker_registry = CircuitBreakerRegistry()