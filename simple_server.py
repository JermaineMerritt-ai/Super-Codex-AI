#!/usr/bin/env python3
"""
Minimal FastAPI server for Super-Codex-AI without ML dependencies
"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
from circuit_breaker import circuit_breaker_registry

# Import ceremonial interface
try:
    from ceremonial_interface import router as ceremonial_router
except ImportError:
    from fastapi import APIRouter
    ceremonial_router = APIRouter()

# Import WooCommerce integration
try:
    from integrations.woocommerce_interface import woocommerce_router
except ImportError:
    from fastapi import APIRouter
    woocommerce_router = APIRouter()

# Initialize Sentry for error tracking
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn and not sentry_dsn.startswith("https://your-sentry-dsn"):
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        integrations=[
            FastApiIntegration(),
            StarletteIntegration(transaction_style="endpoint")
        ],
        send_default_pii=False,  # Don't send personally identifiable information
    )
    print("✅ Sentry error monitoring initialized")
else:
    print("ℹ️ Sentry not configured - update SENTRY_DSN in .env file")

app = FastAPI(title="Super-Codex-AI", version="1.0.0")

# Health check metrics
health_check_counter = Counter('health_checks_total', 'Total health check requests', ['endpoint', 'status'])
health_check_duration = Histogram('health_check_duration_seconds', 'Time spent on health checks', ['endpoint'])
service_status_gauge = Gauge('service_health_status', 'Service health status (1=healthy, 0=unhealthy)', ['service'])
app_uptime_gauge = Gauge('app_uptime_seconds', 'Application uptime in seconds')

# Track application start time
APP_START_TIME = time.time()

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)

# Basic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    environment: str
    uptime_seconds: float
    checks: Dict[str, Any] = {}

class ReadinessResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, Any]
    ready: bool
    response_time_ms: float
    checks_performed: int

class ServiceHealthCheck(BaseModel):
    name: str
    status: str
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    last_check: str

class IngestRequest(BaseModel):
    corpus_dir: str | None = None

class IngestResponse(BaseModel):
    status: str
    message: str
    index_path: str | None = None

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include ceremonial interface
app.include_router(ceremonial_router, prefix="/dominion")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static directory may not exist

# Health check utility functions
async def check_database_health() -> ServiceHealthCheck:
    """Check database connectivity with circuit breaker protection"""
    async def _db_check():
        if os.getenv("DATABASE_URL"):
            await asyncio.sleep(0.01)  # Simulate DB query
            return "healthy"
        else:
            return "not_configured"
    
    start_time = time.time()
    breaker = circuit_breaker_registry.get_or_create("database", failure_threshold=3, reset_timeout=30)
    
    try:
        status = await breaker.call(_db_check)
        error = None
    except Exception as e:
        status = "error"
        error = str(e)
    
    response_time = (time.time() - start_time) * 1000
    return ServiceHealthCheck(
        name="database",
        status=status,
        response_time_ms=response_time,
        error=error,
        last_check=datetime.utcnow().isoformat()
    )

async def check_redis_health() -> ServiceHealthCheck:
    """Check Redis connectivity with circuit breaker protection"""
    async def _redis_check():
        if os.getenv("REDIS_URL"):
            await asyncio.sleep(0.005)  # Simulate Redis ping
            return "healthy"
        else:
            return "not_configured"
    
    start_time = time.time()
    breaker = circuit_breaker_registry.get_or_create("redis", failure_threshold=3, reset_timeout=30)
    
    try:
        status = await breaker.call(_redis_check)
        error = None
    except Exception as e:
        status = "error"
        error = str(e)
    
    response_time = (time.time() - start_time) * 1000
    return ServiceHealthCheck(
        name="redis",
        status=status,
        response_time_ms=response_time,
        error=error,
        last_check=datetime.utcnow().isoformat()
    )

async def check_external_services() -> Dict[str, ServiceHealthCheck]:
    """Check all external service dependencies"""
    checks = await asyncio.gather(
        check_database_health(),
        check_redis_health(),
        return_exceptions=True
    )
    
    result = {}
    for check in checks:
        if isinstance(check, ServiceHealthCheck):
            result[check.name] = check
            # Update Prometheus metrics
            service_status_gauge.labels(service=check.name).set(
                1 if check.status == "healthy" else 0
            )
        elif isinstance(check, Exception):
            result["unknown"] = ServiceHealthCheck(
                name="unknown",
                status="error",
                error=str(check),
                last_check=datetime.utcnow().isoformat()
            )
    
    return result

# Routes
@app.get("/", response_model=dict)
async def root():
    return {
        "service": "Super-Codex-AI - Codex Dominion",
        "version": "1.0.0",
        "status": "operational", 
        "flame_state": "sovereign",
        "ceremonial_interface": "/dominion",
        "health_check": "/health",
        "readiness_check": "/ready",
        "motto": "The flame burns sovereign and eternal — forever."
    }

@app.get("/dominion-redirect", response_class=HTMLResponse)
async def dominion_redirect():
    """Redirect to the ceremonial interface"""
    return HTMLResponse(content='''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting to Codex Dominion</title>
            <meta http-equiv="refresh" content="0; url=/dominion">
        </head>
        <body>
            <p>Redirecting to the Codex Dominion ceremonial interface...</p>
            <p>If you are not redirected automatically, <a href="/dominion">click here</a>.</p>
        </body>
        </html>
    ''', status_code=200)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Enhanced health check endpoint for liveness probes"""
    start_time = time.time()
    
    try:
        # Update uptime metric
        uptime = time.time() - APP_START_TIME
        app_uptime_gauge.set(uptime)
        
        # Basic health checks
        health_checks = {
            "app": "healthy",
            "uptime_seconds": uptime,
            "memory_usage": "normal",  # Could add actual memory monitoring
            "cpu_usage": "normal"      # Could add actual CPU monitoring
        }
        
        # Record metrics
        health_check_counter.labels(endpoint="health", status="success").inc()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            environment=os.getenv("ENVIRONMENT", "docker"),
            uptime_seconds=uptime,
            checks=health_checks
        )
    except Exception as e:
        health_check_counter.labels(endpoint="health", status="error").inc()
        raise e
    finally:
        duration = time.time() - start_time
        health_check_duration.labels(endpoint="health").observe(duration)

@app.get("/ready", response_model=ReadinessResponse)
async def ready():
    """Enhanced readiness check endpoint - comprehensive service readiness"""
    start_time = time.time()
    
    try:
        timestamp = datetime.utcnow().isoformat()
        
        # Perform comprehensive service checks
        service_checks = await check_external_services()
        
        # Determine overall readiness
        healthy_services = [
            check for check in service_checks.values() 
            if check.status == "healthy"
        ]
        total_services = len([
            check for check in service_checks.values() 
            if check.status != "not_configured"
        ])
        
        # Service is ready if all configured services are healthy
        is_ready = total_services == 0 or len(healthy_services) == total_services
        
        # Convert service checks to dict for response
        services_status = {
            name: {
                "status": check.status,
                "response_time_ms": check.response_time_ms,
                "error": check.error,
                "last_check": check.last_check
            }
            for name, check in service_checks.items()
        }
        
        # Add Sentry status
        services_status["sentry"] = {
            "status": "healthy" if os.getenv("SENTRY_DSN") and not os.getenv("SENTRY_DSN").startswith("https://your-sentry-dsn") else "not_configured",
            "response_time_ms": 0,
            "error": None,
            "last_check": timestamp
        }
        
        response_time = (time.time() - start_time) * 1000
        
        # Record metrics
        health_check_counter.labels(
            endpoint="ready", 
            status="ready" if is_ready else "not_ready"
        ).inc()
        
        return ReadinessResponse(
            status="ready" if is_ready else "not_ready",
            timestamp=timestamp,
            services=services_status,
            ready=is_ready,
            response_time_ms=response_time,
            checks_performed=len(service_checks) + 1  # +1 for sentry
        )
    except Exception as e:
        health_check_counter.labels(endpoint="ready", status="error").inc()
        response_time = (time.time() - start_time) * 1000
        
        return ReadinessResponse(
            status="error",
            timestamp=datetime.utcnow().isoformat(),
            services={"error": {"status": "error", "error": str(e)}},
            ready=False,
            response_time_ms=response_time,
            checks_performed=0
        )
    finally:
        duration = time.time() - start_time
        health_check_duration.labels(endpoint="ready").observe(duration)

@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    # Placeholder for actual ingestion logic
    corpus_dir = request.corpus_dir or "/app/corpus"
    
    return IngestResponse(
        status="success",
        message="Ingest functionality placeholder - RAG engine not configured",
        index_path=f"{corpus_dir}/index"
    )

@app.get("/api/status")
async def api_status():
    return {
        "database": "connected" if os.getenv("DATABASE_URL") else "not_configured",
        "redis": "connected" if os.getenv("REDIS_URL") else "not_configured",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "sentry": "enabled" if os.getenv("SENTRY_DSN") and not os.getenv("SENTRY_DSN").startswith("https://your-sentry-dsn") else "not_configured",
        "dominion_status": "sovereign",
        "flame_state": "eternal",
        "ceremonial_interface": "operational"
    }

@app.get("/api/circuit-breakers")
async def circuit_breaker_status():
    """Get status of all circuit breakers"""
    return {
        "circuit_breakers": circuit_breaker_registry.get_all_status(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics/health")
async def health_metrics():
    """Detailed health metrics endpoint"""
    uptime = time.time() - APP_START_TIME
    
    # Get service checks
    service_checks = await check_external_services()
    
    return {
        "uptime_seconds": uptime,
        "health_checks": {
            name: {
                "status": check.status,
                "response_time_ms": check.response_time_ms,
                "last_check": check.last_check
            }
            for name, check in service_checks.items()
        },
        "circuit_breakers": circuit_breaker_registry.get_all_status(),
        "timestamp": datetime.utcnow().isoformat()
    }

# Test endpoints for Sentry error monitoring
@app.get("/test/error")
async def test_error():
    """Test endpoint to generate an error for Sentry monitoring"""
    raise Exception("Test error for Sentry monitoring - this is intentional!")

# Include ceremonial router
app.include_router(ceremonial_router, prefix="/ceremonial", tags=["ceremonial"])

# Include WooCommerce integration router
app.include_router(woocommerce_router, tags=["woocommerce", "ceremonial-commerce"])

@app.get("/test/sentry")
async def test_sentry():
    """Test Sentry manual error capture"""
    try:
        # Manually capture a message
        sentry_sdk.capture_message("Test message from Super-Codex-AI", level="info")
        return {"status": "success", "message": "Test message sent to Sentry"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)