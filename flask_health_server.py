# flask_health_server.py
"""
Comprehensive Flask Health Server for Super-Codex-AI

This Flask application provides health monitoring capabilities
that can run alongside the main FastAPI application.

Features:
- Basic health checks
- Detailed system monitoring  
- Kubernetes-style readiness/liveness probes
- Integration with existing AXIOM flame system
"""
from flask import Flask, jsonify
from flask_cors import CORS
from routes.health import bp as basic_health_bp
from routes.enhanced_health import bp as enhanced_health_bp
import os
import logging

def create_health_app():
    """Factory function to create the Flask health monitoring application."""
    app = Flask(__name__)
    
    # Enable CORS for cross-origin requests
    CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:8010'])
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Register blueprints
    app.register_blueprint(basic_health_bp, url_prefix='/basic')
    app.register_blueprint(enhanced_health_bp)
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'service': 'Super-Codex-AI Health Monitor',
            'flame': 'radiant',
            'status': 'active',
            'version': '1.0.0',
            'endpoints': {
                'basic_health': '/basic/health',
                'health': '/health',
                'detailed_health': '/health/detailed', 
                'liveness': '/health/live',
                'readiness': '/health/ready'
            },
            'integration': {
                'fastapi_server': 'http://127.0.0.1:8010',
                'axiom_flame': 'radiant'
            }
        })
    
    # Integration endpoint to check FastAPI server
    @app.route('/integration/fastapi')
    def check_fastapi_integration():
        """Check if the main FastAPI application is running."""
        import requests
        try:
            response = requests.get('http://127.0.0.1:8010/health/live', timeout=5)
            fastapi_status = {
                'reachable': True,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            fastapi_status = {
                'reachable': False,
                'error': str(e),
                'note': 'FastAPI server may not be running on port 8010'
            }
        
        return jsonify({
            'flask_health': 'active',
            'fastapi_integration': fastapi_status,
            'flame': 'unified' if fastapi_status.get('reachable') else 'seeking_connection'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint not found',
            'flame': 'dimmed',
            'available_endpoints': [
                '/',
                '/basic/health', 
                '/health',
                '/health/detailed',
                '/health/live',
                '/health/ready',
                '/integration/fastapi'
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {error}')
        return jsonify({
            'error': 'Internal server error',
            'flame': 'flickering',
            'message': 'Health monitor encountered an issue'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_health_app()
    
    # Get port from environment or use default
    port = int(os.environ.get('FLASK_PORT', 5001))
    
    print("🔥 Starting Super-Codex-AI Health Monitor")
    print(f"📍 Server running on: http://127.0.0.1:{port}")
    print("🏥 Available health endpoints:")
    print(f"   • Basic Health: http://127.0.0.1:{port}/basic/health")
    print(f"   • Enhanced Health: http://127.0.0.1:{port}/health")
    print(f"   • Detailed Monitoring: http://127.0.0.1:{port}/health/detailed")
    print(f"   • Liveness Probe: http://127.0.0.1:{port}/health/live")
    print(f"   • Readiness Probe: http://127.0.0.1:{port}/health/ready")
    print(f"   • FastAPI Integration: http://127.0.0.1:{port}/integration/fastapi")
    print("🔥 Flame status: RADIANT")
    
    app.run(debug=True, host='127.0.0.1', port=port)