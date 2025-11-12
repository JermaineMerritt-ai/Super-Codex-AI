#!/usr/bin/env python3
"""
Simple test server to verify uvicorn functionality
"""
from fastapi import FastAPI
import uvicorn

# Create a minimal app
app = FastAPI(title="Test Server")

@app.get("/")
async def root():
    return {"message": "Test server is working", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "test-server"}

if __name__ == "__main__":
    print("🧪 Starting Test Server...")
    print("📍 Host: 0.0.0.0")  
    print("🔌 Port: 8010")
    print("=" * 40)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8010,
        log_level="info"
    )