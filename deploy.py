#!/usr/bin/env python3
"""
Unified Artifact System - Production Deployment Script
=====================================================

This script helps deploy the unified artifact system to your production environment.

Usage:
    python deploy.py --env production --config-file production.env
    python deploy.py --env staging --test-webhooks
    python deploy.py --env development --start-server
"""

import argparse
import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

def load_environment_config(config_file: Optional[str] = None) -> Dict[str, str]:
    """Load environment configuration from file"""
    config = {}
    
    if config_file and Path(config_file).exists():
        print(f"📁 Loading config from {config_file}")
        with open(config_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value.strip('"\'')
    else:
        print("⚠️ No config file found, using environment variables")
    
    # Override with environment variables
    env_vars = [
        'CODEX_ENV',
        'CODEX_API_BASE_URL', 
        'CODEX_WEB_BASE_URL',
        'CODEX_COUNCIL_PORTAL_URL',
        'CODEX_PUBLIC_PORTAL_URL',
        'CODEX_AUTH_SCHEME',
        'CODEX_API_KEY_HEADER',
        'CODEX_DATABASE_URL',
        'CODEX_REDIS_URL',
        'CODEX_SIGNATURE_VERIFICATION',
        'CODEX_MAX_FILE_SIZE_MB',
        'CODEX_RATE_LIMIT_PER_MINUTE'
    ]
    
    for var in env_vars:
        if os.getenv(var):
            config[var] = os.getenv(var)
    
    return config

def validate_config(config: Dict[str, str], env: str) -> bool:
    """Validate required configuration for environment"""
    required_for_prod = [
        'CODEX_API_BASE_URL',
        'CODEX_AUTH_SCHEME', 
        'CODEX_DATABASE_URL'
    ]
    
    if env == 'production':
        missing = [key for key in required_for_prod if not config.get(key)]
        if missing:
            print(f"❌ Missing required config for production: {missing}")
            return False
    
    print(f"✅ Configuration valid for {env}")
    return True

def setup_environment(config: Dict[str, str]):
    """Set up environment variables"""
    for key, value in config.items():
        os.environ[key] = value
        print(f"🔧 Set {key}={value}")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    requirements = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0", 
        "aiohttp>=3.9.0",
        "python-multipart>=0.0.6",
        "aiofiles>=23.0.0",
        "pydantic>=2.5.0"
    ]
    
    for package in requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def start_server(env: str, host: str = "0.0.0.0", port: int = 8004):
    """Start the production server"""
    print(f"🚀 Starting server for {env} environment")
    print(f"🌐 Server will be available at http://{host}:{port}")
    
    if env == 'production':
        # Production server with gunicorn or uvicorn workers
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "production_artifact_system:app",
            "--host", host,
            "--port", str(port),
            "--workers", "4",
            "--access-log",
            "--no-reload"
        ]
    else:
        # Development server with hot reload
        cmd = [
            sys.executable, "-m", "uvicorn",
            "production_artifact_system:app", 
            "--host", host,
            "--port", str(port),
            "--reload"
        ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

async def test_webhooks(config: Dict[str, str]):
    """Test webhook connectivity"""
    print("🧪 Testing webhook endpoints...")
    
    import aiohttp
    
    webhook_urls = [
        config.get('CODEX_COUNCIL_PORTAL_URL', '') + '/api/notifications',
        config.get('CODEX_PUBLIC_PORTAL_URL', '') + '/api/broadcasts',
        config.get('CODEX_API_BASE_URL', '') + '/webhooks/replay'
    ]
    
    test_payload = {
        "action": "test_webhook",
        "artifact": {
            "id": "test-webhook",
            "title": "Test Webhook", 
            "type": "test",
            "timestamp": "2025-11-13T08:00:00Z"
        },
        "source": "unified-artifact-system"
    }
    
    async with aiohttp.ClientSession() as session:
        for url in webhook_urls:
            if not url or url.endswith('/'):
                continue
                
            try:
                print(f"🔗 Testing webhook: {url}")
                async with session.post(url, json=test_payload, timeout=10) as response:
                    if response.status < 400:
                        print(f"✅ Webhook {url} responded: {response.status}")
                    else:
                        print(f"⚠️ Webhook {url} error: {response.status}")
            except Exception as e:
                print(f"❌ Webhook {url} failed: {e}")

def create_sample_config():
    """Create a sample configuration file"""
    sample_config = """# Unified Artifact System - Production Configuration
# Copy this file and update with your actual values

# Environment (development, staging, production)
CODEX_ENV=production

# Base URLs - UPDATE THESE WITH YOUR ACTUAL DOMAINS
CODEX_API_BASE_URL=https://api.your-domain.com
CODEX_WEB_BASE_URL=https://your-domain.com
CODEX_COUNCIL_PORTAL_URL=https://council.your-domain.com
CODEX_PUBLIC_PORTAL_URL=https://public.your-domain.com

# Authentication - UPDATE WITH YOUR SCHEME
CODEX_AUTH_SCHEME=bearer  # bearer, api_key, oauth2, sigil_seal
CODEX_API_KEY_HEADER=X-Your-API-Key

# Database - UPDATE WITH YOUR DATABASE
CODEX_DATABASE_URL=postgresql://user:password@your-db-host:5432/artifacts
CODEX_REDIS_URL=redis://your-redis-host:6379/0

# Security
CODEX_SIGNATURE_VERIFICATION=true
CODEX_MAX_FILE_SIZE_MB=50
CODEX_RATE_LIMIT_PER_MINUTE=100

# Optional: SSL/TLS settings for production
# CODEX_SSL_CERT_PATH=/path/to/cert.pem
# CODEX_SSL_KEY_PATH=/path/to/key.pem
"""
    
    with open('production.env.sample', 'w') as f:
        f.write(sample_config)
    
    print("📝 Created sample configuration: production.env.sample")
    print("📝 Copy to production.env and update with your values")

def main():
    """Main deployment script"""
    parser = argparse.ArgumentParser(description="Deploy Unified Artifact System")
    parser.add_argument('--env', choices=['development', 'staging', 'production'], 
                       default='development', help='Deployment environment')
    parser.add_argument('--config-file', help='Configuration file path')
    parser.add_argument('--start-server', action='store_true', 
                       help='Start the server after setup')
    parser.add_argument('--test-webhooks', action='store_true',
                       help='Test webhook connectivity')
    parser.add_argument('--install-deps', action='store_true',
                       help='Install required dependencies')
    parser.add_argument('--create-sample-config', action='store_true',
                       help='Create sample configuration file')
    parser.add_argument('--host', default='0.0.0.0', help='Server host')
    parser.add_argument('--port', type=int, default=8004, help='Server port')
    
    args = parser.parse_args()
    
    print(f"🏭 Unified Artifact System Deployment")
    print(f"🏗️ Environment: {args.env}")
    print("=" * 50)
    
    if args.create_sample_config:
        create_sample_config()
        return
    
    if args.install_deps:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Load configuration
    config = load_environment_config(args.config_file)
    config['CODEX_ENV'] = args.env
    
    # Validate configuration
    if not validate_config(config, args.env):
        print("\n💡 TIP: Run with --create-sample-config to create a template")
        sys.exit(1)
    
    # Set up environment
    setup_environment(config)
    
    if args.test_webhooks:
        print("\n🧪 Testing webhooks...")
        asyncio.run(test_webhooks(config))
    
    if args.start_server:
        print(f"\n🚀 Starting {args.env} server...")
        start_server(args.env, args.host, args.port)
    else:
        print(f"\n✅ Environment configured for {args.env}")
        print(f"🚀 Run with --start-server to start the server")
        print(f"🧪 Run with --test-webhooks to test connectivity")
        
        print(f"\n📋 Quick Start:")
        print(f"python deploy.py --env {args.env} --start-server")

if __name__ == "__main__":
    main()