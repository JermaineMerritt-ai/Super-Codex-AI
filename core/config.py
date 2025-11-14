"""
Core configuration module for the Super-Codex-AI system
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for the Super-Codex-AI system"""
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8080
    environment: str = "development"
    
    # Database settings
    database_url: Optional[str] = None
    
    # Redis settings  
    redis_url: Optional[str] = None
    
    # Security settings
    secret_key: str = "super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Sentry settings
    sentry_dsn: Optional[str] = None
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 1.0
    
    # File storage
    upload_dir: str = "uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    
    # Ceremonial settings
    ceremonial_enabled: bool = True
    axiom_flame_enabled: bool = True
    
    # Rate limiting
    rate_limit_enabled: bool = True
    default_rate_limit: str = "100/hour"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables"""
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8080")),
            environment=os.getenv("ENVIRONMENT", "development"),
            database_url=os.getenv("DATABASE_URL"),
            redis_url=os.getenv("REDIS_URL"),
            secret_key=os.getenv("SECRET_KEY", "super-secret-key-change-in-production"),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_expiration_hours=int(os.getenv("JWT_EXPIRATION_HOURS", "24")),
            sentry_dsn=os.getenv("SENTRY_DSN"),
            sentry_environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
            sentry_traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
            upload_dir=os.getenv("UPLOAD_DIR", "uploads"),
            max_upload_size=int(os.getenv("MAX_UPLOAD_SIZE", "10485760")),
            ceremonial_enabled=os.getenv("CEREMONIAL_ENABLED", "true").lower() == "true",
            axiom_flame_enabled=os.getenv("AXIOM_FLAME_ENABLED", "true").lower() == "true",
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            default_rate_limit=os.getenv("DEFAULT_RATE_LIMIT", "100/hour"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "json"),
        )


# Global configuration instance
config = Config.from_env()


def get_config() -> Config:
    """Get the global configuration instance"""
    return config


def update_config(**kwargs):
    """Update configuration values"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)


def get_database_config() -> Dict[str, Any]:
    """Get database configuration"""
    return {
        "url": config.database_url,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    }


def get_redis_config() -> Dict[str, Any]:
    """Get Redis configuration"""
    return {
        "url": config.redis_url,
        "decode_responses": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5,
        "health_check_interval": 30,
    }


def get_sentry_config() -> Dict[str, Any]:
    """Get Sentry configuration"""
    return {
        "dsn": config.sentry_dsn,
        "environment": config.sentry_environment,
        "traces_sample_rate": config.sentry_traces_sample_rate,
        "send_default_pii": False,
        "attach_stacktrace": True,
    }


def is_production() -> bool:
    """Check if running in production environment"""
    return config.environment.lower() == "production"


def is_development() -> bool:
    """Check if running in development environment"""
    return config.environment.lower() == "development"


def is_testing() -> bool:
    """Check if running in test environment"""
    return config.environment.lower() == "test"