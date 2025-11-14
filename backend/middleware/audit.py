import os
import json
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./data/audit.log")

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)

        # Build audit entry
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
            "status_code": response.status_code,
            "headers": dict(request.headers),
        }

        # Append to immutable log
        try:
            with open(AUDIT_LOG_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            # Fail silently but never block request
            print(f"Audit log error: {e}")

        return response