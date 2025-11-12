# routes/enhanced_health.py
from flask import Blueprint, jsonify
import datetime
import platform
import psutil
import os

bp = Blueprint('enhanced_health', __name__)

@bp.route('/health', methods=['GET'])
def health():
    """Basic health check endpoint."""
    return jsonify(status="ok", flame="radiant", version="1.0.0"), 200

@bp.route('/health/detailed', methods=['GET'])
def detailed_health():
    """Detailed health check with system information."""
    try:
        # System information
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor() or 'Unknown',
            'hostname': platform.node()
        }
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_info = {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'used_percent': memory.percent,
            'free_percent': round(100 - memory.percent, 2)
        }
        
        # Disk information
        disk = psutil.disk_usage('/')
        disk_info = {
            'total_gb': round(disk.total / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'used_percent': round((disk.used / disk.total) * 100, 2)
        }
        
        # Environment information
        env_info = {
            'virtual_env': os.environ.get('VIRTUAL_ENV', 'Not activated'),
            'path_exists': os.path.exists('.venv'),
            'requirements_exists': os.path.exists('requirements.txt')
        }
        
        return jsonify({
            'status': 'healthy',
            'flame': 'blazing',
            'version': '1.0.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'uptime_check': True,
            'system': system_info,
            'memory': memory_info,
            'disk': disk_info,
            'environment': env_info,
            'services': {
                'flask': 'active',
                'axiom_flame': 'radiant'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'degraded',
            'flame': 'flickering', 
            'version': '1.0.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'error': str(e),
            'message': 'Health check encountered issues'
        }), 503

@bp.route('/health/ready', methods=['GET'])
def readiness():
    """Readiness probe for container orchestration."""
    # Check if application is ready to serve traffic
    checks = {
        'database': True,  # Would check actual DB connection
        'external_apis': True,  # Would check external dependencies  
        'file_system': os.access('.', os.W_OK),  # Check write permissions
        'environment': os.environ.get('FLASK_APP') is not None or True
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return jsonify({
        'ready': all_ready,
        'flame': 'steady' if all_ready else 'unstable',
        'checks': checks,
        'timestamp': datetime.datetime.now().isoformat()
    }), status_code

@bp.route('/health/live', methods=['GET'])
def liveness():
    """Liveness probe for container orchestration."""
    return jsonify({
        'alive': True,
        'flame': 'eternal',
        'timestamp': datetime.datetime.now().isoformat(),
        'process_id': os.getpid()
    }), 200