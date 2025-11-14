#!/usr/bin/env python3
"""
Enhanced Sovereign Commerce Platform Startup Server
Launching the complete diaspora funder platform with all enhancements

Built with ceremonial dignity for the diaspora community.
"""

import logging
import sys
import os
import asyncio
import uvicorn
from pathlib import Path

# Add the services directory to the path
services_dir = Path(__file__).parent / "services"
sys.path.insert(0, str(services_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SOVEREIGN-COMMERCE - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sovereign_commerce.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Launch the enhanced Sovereign Commerce platform"""
    
    logger.info("🔥 Starting Enhanced Sovereign Commerce Platform")
    logger.info("🌍 Diaspora Funder Platform with Cultural Recognition")
    
    # Environment checks
    logger.info("🔍 Performing environment checks...")
    
    # Check if database directory exists
    current_dir = Path(__file__).parent
    db_dir = current_dir / 'db'
    db_dir.mkdir(exist_ok=True)
    logger.info(f"📂 Database directory: {db_dir}")
    
    # Check template and static directories
    template_dir = current_dir / "ui" / "templates"
    static_dir = current_dir / "ui" / "static"
    
    if not template_dir.exists():
        logger.warning(f"⚠️  Template directory not found: {template_dir}")
        logger.info("ℹ️  Creating basic template directory structure...")
        template_dir.mkdir(parents=True, exist_ok=True)
    
    if not static_dir.exists():
        logger.warning(f"⚠️  Static directory not found: {static_dir}")
        logger.info("ℹ️  Creating basic static directory structure...")
        static_dir.mkdir(parents=True, exist_ok=True)
    
    # Import and configure the app
    try:
        from sovereign_main import app
        logger.info("✅ Sovereign Commerce application imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import application: {e}")
        sys.exit(1)
    
    # Server configuration
    host = os.getenv("SOVEREIGN_COMMERCE_HOST", "127.0.0.1")
    port = int(os.getenv("SOVEREIGN_COMMERCE_PORT", "8080"))
    workers = int(os.getenv("SOVEREIGN_COMMERCE_WORKERS", "1"))
    reload = os.getenv("SOVEREIGN_COMMERCE_RELOAD", "true").lower() == "true"
    
    logger.info(f"🌐 Server configuration:")
    logger.info(f"   Host: {host}")
    logger.info(f"   Port: {port}")
    logger.info(f"   Workers: {workers}")
    logger.info(f"   Reload: {reload}")
    
    # Enhanced features banner
    logger.info("🎯 Enhanced Features Enabled:")
    logger.info("   📦 Enhanced Product Catalog with Cultural Context")
    logger.info("   🛒 Advanced Checkout System with Community Funds")
    logger.info("   📊 Diaspora Funder Dashboard with Insights")
    logger.info("   🏆 Contributor Recognition System with Honors")
    logger.info("   🔗 AXIOM-FLAME Integration for Ceremonial Operations")
    
    # API endpoints summary
    logger.info("🔌 Enhanced API Endpoints Available:")
    logger.info("   /api/enhanced/catalog/*      - Enhanced product catalog")
    logger.info("   /api/enhanced/checkout/*     - Advanced checkout system")
    logger.info("   /api/enhanced/dashboard/*    - Funder dashboard")
    logger.info("   /api/enhanced/recognition/*  - Contributor recognition")
    logger.info("   /api/enhanced/status         - System status")
    logger.info("   /api/enhanced/initialize     - Initialize sample data")
    
    # Launch server
    try:
        logger.info("🚀 Launching Enhanced Sovereign Commerce Platform...")
        logger.info("📖 API Documentation available at: http://127.0.0.1:8080/sacred/docs")
        logger.info("🔥 Platform ready to serve the diaspora community!")
        
        # Use uvicorn to run the server
        uvicorn.run(
            "sovereign_main:app",
            host=host,
            port=port,
            workers=workers if not reload else 1,  # Workers > 1 incompatible with reload
            reload=reload,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown requested")
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        sys.exit(1)
    
    logger.info("👋 Enhanced Sovereign Commerce Platform shutdown complete")

if __name__ == "__main__":
    main()