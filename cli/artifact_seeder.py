#!/usr/bin/env python3
"""
Codex Artifact Seeder - CLI tool for seeding core constitutional artifacts

This script creates and seals fundamental governance documents in the Codex system:
- Constitution: The foundational governance document
- Eternal Charter: The perpetual operational charter
- Public Release Proclamation: The official public release declaration

Usage:
    python cli/artifact_seeder.py

Environment Variables:
    API_URL: Base URL for the Codex API (default: https://codexdominion.app/v1)
    CLI_API_KEY: API key for authentication (required)
"""

import requests
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "https://codexdominion.app/v1")
CLI_API_KEY = os.getenv("CLI_API_KEY")

# Request headers with authentication
HEADERS = {"Authorization": f"Bearer {CLI_API_KEY}"}

def validate_environment():
    """Validate required environment variables are set."""
    if not CLI_API_KEY:
        print("❌ Error: CLI_API_KEY environment variable is required")
        sys.exit(1)
    
    print(f"🔧 Using API endpoint: {API_URL}")

def create_and_seal_artifact(title: str, slug: str, type_: str, content_uri: str) -> Dict[str, Any]:
    """
    Create an artifact and immediately seal it.
    
    Args:
        title: Human-readable title of the artifact
        slug: URL-friendly identifier
        type_: Artifact type (Constitution, Charter, Proclamation)
        content_uri: URI pointing to the artifact content
    
    Returns:
        Dict containing the sealed artifact details
    """
    try:
        # Step 1: Create artifact
        payload = {
            "title": title,
            "slug": slug,
            "type": type_,
            "content_uri": content_uri
        }
        
        print(f"📝 Creating {type_}: {title}")
        r = requests.post(f"{API_URL}/artifacts", json=payload, headers=HEADERS)
        r.raise_for_status()
        artifact = r.json()
        print(f"✅ Created {type_}: {artifact['id']}")

        # Step 2: Seal artifact
        print(f"🔒 Sealing {type_}...")
        seal_url = f"{API_URL}/artifacts/{artifact['id']}/seal"
        r = requests.post(seal_url, headers=HEADERS)
        r.raise_for_status()
        sealed = r.json()
        print(f"🏆 Sealed {type_}: {sealed['title']} v{sealed['version']}")

        return sealed
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error processing {type_}: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error with {type_}: {e}")
        raise

def main():
    """Main seeding function that creates all core artifacts."""
    print("🌐 Seeding Codex core artifacts...")
    print("=" * 50)
    
    # Validate environment before proceeding
    validate_environment()
    
    try:
        # Core constitutional documents
        artifacts = []
        
        # Constitution - The foundational governance document
        constitution = create_and_seal_artifact(
            title="Codex Constitution",
            slug="constitution",
            type_="Constitution",
            content_uri="uploads/constitution.pdf"
        )
        artifacts.append(constitution)
        print()

        # Eternal Charter - The perpetual operational charter
        charter = create_and_seal_artifact(
            title="Eternal Charter",
            slug="eternal-charter",
            type_="Charter",
            content_uri="uploads/charter.pdf"
        )
        artifacts.append(charter)
        print()

        # Public Release Proclamation - Official public release declaration
        proclamation = create_and_seal_artifact(
            title="Public Release Proclamation",
            slug="public-proclamation",
            type_="Proclamation",
            content_uri="uploads/proclamation.pdf"
        )
        artifacts.append(proclamation)
        print()

        # Summary
        print("=" * 50)
        print("✅ Core artifacts seeded and sealed successfully!")
        print(f"📊 Total artifacts processed: {len(artifacts)}")
        
        for artifact in artifacts:
            print(f"   • {artifact['title']} v{artifact['version']} ({artifact.get('id', 'N/A')})")
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()