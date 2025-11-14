from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Example usage in FastAPI route:
# @app.get("/secure")
# @limiter.limit("5/minute")

# Basic rate limiting
@app.get("/api/query")
@limiter.limit("10/minute")
async def query_endpoint():
    pass

# Stricter limits for sensitive endpoints
@app.post("/api/admin")
@limiter.limit("2/minute")
async def admin_endpoint():
    pass