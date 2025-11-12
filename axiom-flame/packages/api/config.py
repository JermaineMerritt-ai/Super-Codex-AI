"""
Flask Configuration for Axiom-Flame API
"""
import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'axiom-flame-secret-key-for-development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API settings
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5010))
    
    # Axiom-Flame specific paths
    BASE_PATH = Path(__file__).parent.parent.parent  # axiom-flame root
    STORAGE_PATH = BASE_PATH / "storage"
    ARTIFACTS_PATH = BASE_PATH / "artifacts"
    SCHEMAS_PATH = ARTIFACTS_PATH / "schemas"
    LEDGER_PATH = STORAGE_PATH / "ledger"
    REPLAYS_PATH = STORAGE_PATH / "replays"
    ANNALS_PATH = STORAGE_PATH / "annals"
    
    # Ensure directories exist
    @classmethod
    def init_directories(cls):
        """Create necessary directories"""
        for path_attr in ['STORAGE_PATH', 'LEDGER_PATH', 'REPLAYS_PATH', 'ANNALS_PATH']:
            path = getattr(cls, path_attr)
            path.mkdir(parents=True, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False