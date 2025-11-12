#!/usr/bin/env python3
"""
Simple Flask Test Server
"""
from flask import Flask, jsonify
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'axiom-flame-test',
        'message': 'Server is working!'
    })

@app.route('/')
def index():
    return jsonify({
        'service': 'axiom-flame-api',
        'status': 'running',
        'endpoints': ['/health', '/status']
    })

if __name__ == '__main__':
    print("🔥 Starting simple Flask test server...")
    print("🌐 Server will be available at: http://127.0.0.1:8088")
    print("💚 Test URL: http://127.0.0.1:8088/health")
    
    try:
        app.run(host='127.0.0.1', port=8088, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Server failed: {e}")
        sys.exit(1)