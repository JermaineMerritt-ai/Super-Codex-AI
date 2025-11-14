#!/usr/bin/env python3
"""
Deployment script for Sovereign Commerce Platform
Designed for diaspora funders with ceremonial elements
"""

import os
import sys
import subprocess
from pathlib import Path

def create_virtual_environment():
    """Create and activate Python virtual environment"""
    print("🔥 Creating ceremonial environment...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    print("✨ Virtual environment created")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing sacred dependencies...")
    requirements = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.0",
        "passlib[bcrypt]>=1.7.4",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.2",
        "aiofiles>=23.2.1"
    ]
    
    for package in requirements:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    print("✅ Dependencies installed")

def setup_database():
    """Initialize the database with ceremonial schema"""
    print("🏛️ Establishing sacred database...")
    db_path = Path("db/sovereign_commerce.db")
    if not db_path.exists():
        # Create database using schema
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        
        with open("db/schema.sql", "r") as schema_file:
            conn.executescript(schema_file.read())
        
        conn.close()
        print("✨ Database consecrated")
    else:
        print("📖 Database already exists")

def seed_ceremonial_data():
    """Seed the database with initial ceremonial data"""
    print("🌱 Seeding ceremonial data...")
    subprocess.run([sys.executable, "ops/seed_data.py"], check=True)
    print("🌟 Sacred offerings prepared")

def generate_sovereign_keys():
    """Generate ceremonial signing keys"""
    print("🗝️ Forging sovereign keys...")
    import secrets
    
    # Generate JWT secret key
    jwt_secret = secrets.token_urlsafe(32)
    
    # Create environment file
    env_content = f"""# Sovereign Commerce Environment Configuration
# Generated on deployment for diaspora funders

# Authentication
JWT_SECRET_KEY="{jwt_secret}"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL="sqlite:///./db/sovereign_commerce.db"

# Platform Configuration
PLATFORM_NAME="Sovereign Commerce"
PLATFORM_VERSION="1.0.0"
ARTIFACT_ID="codex-build-0001"

# Ceremonial Settings
SIGIL_PREFIX="SGN"
CEREMONIAL_AUTHORITY="Council-Prime"
SOVEREIGNTY_LEVEL="Diaspora-Recognition"

# Engine Integration
AXIOM_ENABLED=true
RAG_ENABLED=true
SIGIL_ENABLED=true
ORACLE_ENABLED=true
LANTERN_ENABLED=true
FLAME_ENABLED=true
"""
    
    with open(".env", "w") as env_file:
        env_file.write(env_content)
    
    print("🏆 Sovereign keys forged")

def update_main_paths():
    """Update main.py to use new directory structure"""
    print("🔧 Updating ceremonial pathways...")
    
    # Update template and static file paths in main.py
    main_py_path = "services/main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as f:
            content = f.read()
        
        # Update paths to new structure
        content = content.replace('templates"', 'ui/templates"')
        content = content.replace('static"', 'ui/static"')
        content = content.replace('sovereign_commerce.db', 'db/sovereign_commerce.db')
        
        with open(main_py_path, "w") as f:
            f.write(content)
        
        print("✨ Pathways consecrated")

def deploy():
    """Complete deployment process"""
    print("🚀 Initiating Sovereign Commerce deployment for diaspora funders...")
    print("=" * 60)
    
    try:
        create_virtual_environment()
        install_dependencies()
        setup_database()
        generate_sovereign_keys()
        update_main_paths()
        seed_ceremonial_data()
        
        print("=" * 60)
        print("✅ Sovereign Commerce Platform successfully deployed!")
        print()
        print("🎯 Next steps:")
        print("   1. Activate virtual environment: .venv\\Scripts\\Activate.ps1")
        print("   2. Start the platform: uvicorn services.main:app --host 127.0.0.1 --port 8080 --reload")
        print("   3. Access the platform: http://127.0.0.1:8080")
        print()
        print("🏛️ Platform configured for:")
        print("   • Diaspora Funders")
        print("   • Heirs and Councils") 
        print("   • Custodians and Flamekeepers")
        print("   • Sovereign Recognition System")
        print()
        print("🔥 May the ceremony begin!")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()