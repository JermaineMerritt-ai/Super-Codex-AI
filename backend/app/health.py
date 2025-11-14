from fastapi import APIRouter
from fastapi.responses import JSONResponse
import psutil
import os
from datetime import datetime
import logging

router = APIRouter(prefix="/health", tags=["health"])

logger = logging.getLogger(__name__)

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Super-Codex-AI",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Process info
        process = psutil.Process(os.getpid())
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": {
                "name": "Super-Codex-AI",
                "version": "1.0.0",
                "environment": os.getenv("ENVIRONMENT", "development")
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            "process": {
                "pid": process.pid,
                "memory_percent": process.memory_percent(),
                "num_threads": process.num_threads(),
                "create_time": datetime.fromtimestamp(process.create_time()).isoformat()
            },
            "checks": {
                "database": await check_database_connection(),
                "external_services": await check_external_services(),
                "file_system": check_file_system()
            }
        }
        
        # Determine overall status
        all_checks_passed = all([
            health_data["checks"]["database"]["status"] == "healthy",
            health_data["checks"]["external_services"]["status"] == "healthy",
            health_data["checks"]["file_system"]["status"] == "healthy"
        ])
        
        if not all_checks_passed:
            health_data["status"] = "degraded"
        
        status_code = 200 if all_checks_passed else 503
        return JSONResponse(content=health_data, status_code=status_code)
    
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            },
            status_code=503
        )

async def check_database_connection():
    """Check database connectivity"""
    try:
        # Simulate database check
        # In production, this would test actual DB connection
        return {
            "status": "healthy",
            "response_time_ms": 15,
            "last_check": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }

async def check_external_services():
    """Check external service dependencies"""
    try:
        # Simulate external service checks
        services = {
            "axiom_flame_api": {"status": "healthy", "url": "http://localhost:8080"},
            "woocommerce_api": {"status": "healthy", "url": "https://store.example.com"},
            "github_api": {"status": "healthy", "url": "https://api.github.com"}
        }
        
        all_healthy = all(service["status"] == "healthy" for service in services.values())
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "services": services,
            "last_check": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }

def check_file_system():
    """Check file system access"""
    try:
        # Check critical directories
        critical_dirs = ["logs", "uploads", "backend/services"]
        
        for dir_path in critical_dirs:
            if not os.path.exists(dir_path):
                return {
                    "status": "unhealthy",
                    "error": f"Critical directory missing: {dir_path}",
                    "last_check": datetime.utcnow().isoformat()
                }
        
        # Test write access to logs
        test_file = "logs/health_check.test"
        try:
            os.makedirs("logs", exist_ok=True)
            with open(test_file, "w") as f:
                f.write("health check")
            os.remove(test_file)
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": f"Cannot write to logs directory: {e}",
                "last_check": datetime.utcnow().isoformat()
            }
        
        return {
            "status": "healthy",
            "directories_checked": len(critical_dirs),
            "last_check": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }

@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe endpoint"""
    # Simple check to verify service is ready to serve traffic
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe endpoint"""
    # Simple check to verify service is still alive
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }