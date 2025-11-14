#!/usr/bin/env python3
"""
Simple server test to identify issues.
"""

import asyncio
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Simple Test API")

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting simple test server...")
    print("Testing on http://127.0.0.1:8083")
    
    try:
        uvicorn.run(
            "simple_server_test:app",
            host="127.0.0.1",
            port=8083,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()