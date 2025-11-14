#!/usr/bin/env python3
"""
Main entry point for the Super-Codex-AI server
Comprehensive ceremonial interface system
"""
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from prometheus_fastapi_instrumentator import Instrumentator

# Import local modules
try:
    from simple_server import app as simple_app, ceremonial_router
except ImportError:
    # Create minimal app if simple_server is not available
    simple_app = FastAPI(title="Super-Codex-AI", version="1.0.0")
    ceremonial_router = None

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8081"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Initialize Sentry if DSN is provided
if SENTRY_DSN and SENTRY_DSN.startswith("https://"):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            FastApiIntegration(auto_enabling_integrations=False),
        ],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        environment=os.getenv("SENTRY_ENVIRONMENT", ENVIRONMENT),
    )
    print("✅ Sentry initialized")
else:
    print("ℹ️ Sentry not configured - update SENTRY_DSN in .env file")

# Create main app
app = FastAPI(
    title="Super-Codex-AI System",
    description="Comprehensive ceremonial interface and dashboard system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount simple server routes if available
if hasattr(simple_app, "routes"):
    for route in simple_app.routes:
        if hasattr(route, "path") and not route.path.startswith("/static"):
            app.mount("/", simple_app)
            break

# Initialize Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/metrics")

# Templates setup
templates_dir = Path("templates")
if templates_dir.exists():
    templates = Jinja2Templates(directory="templates")
else:
    # Create templates directory and basic template
    templates_dir.mkdir(exist_ok=True)
    basic_template = """<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; }
        .status { padding: 10px; border-radius: 4px; margin: 10px 0; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{title}}</h1>
        <div class="status success">{{message}}</div>
        {% if links %}
        <h2>Available Interfaces:</h2>
        <ul>
        {% for link in links %}
            <li><a href="{{link.url}}">{{link.name}}</a></li>
        {% endfor %}
        </ul>
        {% endif %}
    </div>
</body>
</html>"""
    
    with open(templates_dir / "base.html", "w") as f:
        f.write(basic_template)
    
    templates = Jinja2Templates(directory="templates")

# Static files setup
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main landing page with system overview"""
    links = [
        {"name": "System Health Check", "url": "/health"},
        {"name": "API Documentation", "url": "/docs"},
        {"name": "Metrics", "url": "/metrics"},
        {"name": "Ceremonial Interface", "url": "/ceremonial"},
        {"name": "Dominion Portal", "url": "/dominion"},
        {"name": "Command Center", "url": "/command"},
    ]
    
    return templates.TemplateResponse("base.html", {
        "request": request,
        "title": "Super-Codex-AI System",
        "message": "🌟 Super-Codex-AI system is operational and ready for ceremonial operations!",
        "links": links
    })

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "message": "Super-Codex-AI system is operational",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "timestamp": "2025-01-27T13:45:00Z"
    }

# System status endpoint
@app.get("/status")
async def system_status():
    """Detailed system status"""
    return {
        "system": "Super-Codex-AI",
        "status": "operational",
        "components": {
            "ceremonial_interface": "active",
            "dashboard_system": "active",
            "metrics_collection": "active",
            "health_monitoring": "active"
        },
        "environment": ENVIRONMENT,
        "host": HOST,
        "port": PORT
    }

# Ceremonial interface placeholder
@app.get("/ceremonial", response_class=HTMLResponse)
async def ceremonial_interface(request: Request):
    """Ceremonial interface placeholder"""
    return templates.TemplateResponse("base.html", {
        "request": request,
        "title": "Ceremonial Interface",
        "message": "🔥 Ceremonial interface is ready for ceremonial operations.",
        "links": [
            {"name": "Back to Main", "url": "/"},
            {"name": "System Health", "url": "/health"}
        ]
    })

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

# Include ceremonial router if available
if ceremonial_router:
    try:
        app.include_router(ceremonial_router, prefix="/api/ceremonial")
    except Exception as e:
        print(f"Warning: Could not include ceremonial router: {e}")

def main():
    """Main function to run the server"""
    print(f"🚀 Starting Super-Codex-AI server...")
    print(f"📍 Environment: {ENVIRONMENT}")
    print(f"🌐 Server will be available at: http://{HOST}:{PORT}")
    print(f"📚 API docs available at: http://{HOST}:{PORT}/docs")
    
    try:
        uvicorn.run(
            "main:app",
            host=HOST,
            port=PORT,
            reload=ENVIRONMENT == "development",
            workers=1,  # Use 1 worker for Windows compatibility
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
