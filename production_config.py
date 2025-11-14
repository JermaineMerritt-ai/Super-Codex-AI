"""
Production Configuration for Unified Artifact Management System
==============================================================

This module provides production-ready configuration with:
- Environment-specific settings
- Authentication schemes
- Security configurations
- Integration patterns for councils and public portals
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    """Deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class AuthScheme(Enum):
    """Supported authentication schemes"""
    BEARER_TOKEN = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    SIGIL_SEAL = "sigil_seal"

@dataclass
class ProductionConfig:
    """Production configuration settings"""
    
    # Environment
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    
    # Base URLs
    api_base_url: str = "https://api.codexdominion.app"
    web_base_url: str = "https://codexdominion.app"
    council_portal_url: str = "https://council.codexdominion.app"
    public_portal_url: str = "https://public.codexdominion.app"
    
    # Authentication
    auth_scheme: AuthScheme = AuthScheme.SIGIL_SEAL
    api_key_header: str = "X-Codex-API-Key"
    sigil_verification_endpoint: str = "/auth/verify-sigil"
    
    # Security
    allowed_origins: List[str] = None
    rate_limit_per_minute: int = 100
    max_file_size_mb: int = 50
    signature_verification: bool = True
    
    # Database
    database_url: str = "postgresql://codex:secure@localhost:5432/codex_artifacts"
    redis_url: str = "redis://localhost:6379/0"
    
    # Storage
    artifact_storage_path: str = "/var/codex/artifacts"
    backup_storage_path: str = "/var/codex/backups"
    
    # Replay Integration
    replay_webhook_url: str = "https://api.codexdominion.app/webhooks/replay"
    council_notification_url: str = "https://council.codexdominion.app/api/notifications"
    public_broadcast_url: str = "https://public.codexdominion.app/api/broadcasts"
    
    def __post_init__(self):
        """Initialize derived settings"""
        if self.allowed_origins is None:
            self.allowed_origins = [
                self.web_base_url,
                self.council_portal_url,
                self.public_portal_url
            ]

# Environment-specific configurations
CONFIGS = {
    Environment.DEVELOPMENT: ProductionConfig(
        environment=Environment.DEVELOPMENT,
        debug=True,
        api_base_url="http://localhost:8004",
        web_base_url="http://localhost:3000",
        council_portal_url="http://localhost:3001",
        public_portal_url="http://localhost:3002",
        auth_scheme=AuthScheme.BEARER_TOKEN,
        signature_verification=False,
        rate_limit_per_minute=1000,
        database_url="sqlite:///./artifacts_dev.db",
        redis_url="redis://localhost:6379/1"
    ),
    
    Environment.STAGING: ProductionConfig(
        environment=Environment.STAGING,
        debug=False,
        api_base_url="https://api-staging.codexdominion.app",
        web_base_url="https://staging.codexdominion.app",
        council_portal_url="https://council-staging.codexdominion.app",
        public_portal_url="https://public-staging.codexdominion.app",
        auth_scheme=AuthScheme.SIGIL_SEAL,
        signature_verification=True,
        rate_limit_per_minute=200
    ),
    
    Environment.PRODUCTION: ProductionConfig(
        environment=Environment.PRODUCTION,
        debug=False,
        signature_verification=True,
        rate_limit_per_minute=100
    )
}

def get_config(env: Optional[Environment] = None) -> ProductionConfig:
    """Get configuration for specified environment"""
    if env is None:
        env_name = os.getenv("CODEX_ENV", "development").lower()
        env = Environment(env_name)
    
    config = CONFIGS.get(env, CONFIGS[Environment.DEVELOPMENT])
    
    # Override with environment variables if present
    if os.getenv("CODEX_API_BASE_URL"):
        config.api_base_url = os.getenv("CODEX_API_BASE_URL")
    
    if os.getenv("CODEX_AUTH_SCHEME"):
        config.auth_scheme = AuthScheme(os.getenv("CODEX_AUTH_SCHEME"))
    
    if os.getenv("CODEX_DATABASE_URL"):
        config.database_url = os.getenv("CODEX_DATABASE_URL")
    
    return config

# Authentication configuration for different schemes
AUTH_CONFIGS = {
    AuthScheme.BEARER_TOKEN: {
        "header_name": "Authorization",
        "header_prefix": "Bearer ",
        "validation_endpoint": "/auth/validate-token"
    },
    
    AuthScheme.API_KEY: {
        "header_name": "X-Codex-API-Key",
        "validation_endpoint": "/auth/validate-key"
    },
    
    AuthScheme.OAUTH2: {
        "token_url": "/auth/token",
        "scopes": {
            "artifacts:read": "Read artifacts",
            "artifacts:write": "Create and modify artifacts",
            "artifacts:admin": "Administrative access to artifacts"
        }
    },
    
    AuthScheme.SIGIL_SEAL: {
        "header_name": "X-Codex-Sigil",
        "verification_endpoint": "/auth/verify-sigil",
        "seal_authority_required": "COUNCIL",
        "binding_strength_minimum": 50
    }
}

# Route configuration for different portals
PORTAL_ROUTES = {
    "council": {
        "base_path": "/council/api/v1",
        "allowed_operations": ["read", "write", "admin", "replay"],
        "required_authority": "COUNCIL",
        "rate_limit": 200
    },
    
    "public": {
        "base_path": "/public/api/v1",
        "allowed_operations": ["read", "replay"],
        "required_authority": "PUBLIC",
        "rate_limit": 50
    },
    
    "admin": {
        "base_path": "/admin/api/v1",
        "allowed_operations": ["read", "write", "admin", "replay", "system"],
        "required_authority": "SUPREME",
        "rate_limit": 500
    }
}

# Webhook configuration for replay triggers
REPLAY_WEBHOOKS = {
    "council_notification": {
        "url": "https://council.codexdominion.app/api/notifications",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-Codex-Source": "artifact-system"
        },
        "retry_attempts": 3
    },
    
    "public_broadcast": {
        "url": "https://public.codexdominion.app/api/broadcasts",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-Codex-Source": "artifact-system"
        },
        "retry_attempts": 3
    },
    
    "replay_archive": {
        "url": "https://api.codexdominion.app/webhooks/replay",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-Codex-Source": "artifact-system"
        },
        "retry_attempts": 5
    }
}

def get_auth_config(scheme: AuthScheme) -> Dict:
    """Get authentication configuration for scheme"""
    return AUTH_CONFIGS.get(scheme, AUTH_CONFIGS[AuthScheme.BEARER_TOKEN])

def get_portal_routes(portal: str) -> Dict:
    """Get route configuration for portal"""
    return PORTAL_ROUTES.get(portal, PORTAL_ROUTES["public"])

def get_replay_webhook(webhook_type: str) -> Dict:
    """Get webhook configuration for replay triggers"""
    return REPLAY_WEBHOOKS.get(webhook_type, REPLAY_WEBHOOKS["replay_archive"])