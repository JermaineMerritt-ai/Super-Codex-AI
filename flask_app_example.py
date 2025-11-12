# flask_app_example.py
"""
Example Flask application using the health blueprint.
This demonstrates how to integrate the Flask health route.
"""
from flask import Flask
from routes.health import bp as health_bp

def create_app():
    """Factory function to create Flask application."""
    app = Flask(__name__)
    
    # Register the health blueprint
    app.register_blueprint(health_bp)
    
    # Add a simple root route
    @app.route('/')
    def root():
        return {
            'message': 'Super-Codex-AI Flask API',
            'flame': 'radiant',
            'status': 'active'
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🔥 Starting Flask application with health routes...")
    print("📍 Health endpoint: http://127.0.0.1:5000/health")
    print("🏠 Root endpoint: http://127.0.0.1:5000/")
    app.run(debug=True, host='127.0.0.1', port=5000)