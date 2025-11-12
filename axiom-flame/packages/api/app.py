from flask import Flask
from routes import register_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_directories()
    register_routes(app)
    return app

app = create_app()

def start_server(host=None, port=None, debug=None):
    """Start the Flask server with proper configuration."""
    try:
        host = host or Config.HOST
        port = port or Config.PORT
        debug = debug if debug is not None else Config.DEBUG
        
        print(f"[FLAME] Starting Axiom-Flame Ceremonial API on {host}:{port}...")
        print(f"[INFO] Available endpoints: {len(app.url_map._rules)} routes configured")
        print(f"[CONFIG] Debug mode: {debug}")
        print(f"[READY] Server ready for ceremonial operations")
        
        app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"[ERROR] Failed to start Axiom-Flame API: {e}")
        return False
    return True

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else Config.PORT
    start_server(port=port)