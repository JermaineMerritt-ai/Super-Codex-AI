#!/usr/bin/env python3
"""
Codex Ceremony Scheduler - CLI tool for scheduling and managing Codex induction ceremonies

This script manages the complete ceremony lifecycle:
- Schedule induction ceremonies
- Start ceremonies
- Record heir oaths and signatures
- Close and archive ceremonies

Usage:
    python cli/ceremony_scheduler.py

Environment Variables:
    API_URL: Base URL for the Codex API (default: https://codexdominion.app/v1)
    CLI_API_KEY: API key for authentication (required)
"""

import requests
import os
import sys
from datetime import datetime
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

def schedule_induction(ceremony_id="induction-001", location="Codex Hall", council_id="council-root"):
    """
    Schedule a new induction ceremony.
    
    Args:
        ceremony_id: Unique identifier for the ceremony
        location: Physical or virtual location for the ceremony
        council_id: Council responsible for the ceremony
    
    Returns:
        Dict containing the scheduled ceremony details
    """
    try:
        payload = {
            "kind": "Induction",
            "script_ref": "ceremonies/induction_script.json",
            "scheduled_at": datetime.utcnow().isoformat(),
            "location": location,
            "council_id": council_id
        }
        
        print(f"📅 Scheduling induction ceremony at {location}")
        r = requests.post(f"{API_URL}/ceremonies", json=payload, headers=HEADERS)
        r.raise_for_status()
        ceremony = r.json()
        print(f"📜 Scheduled Induction Ceremony: {ceremony['id']}")
        return ceremony
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scheduling ceremony: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error scheduling ceremony: {e}")
        raise

def start_ceremony(ceremony_id):
    """
    Start a scheduled ceremony.
    
    Args:
        ceremony_id: ID of the ceremony to start
    """
    try:
        print(f"🚀 Starting ceremony {ceremony_id}")
        r = requests.post(f"{API_URL}/ceremonies/{ceremony_id}/start", headers=HEADERS)
        r.raise_for_status()
        print(f"🔥 Ceremony {ceremony_id} started successfully")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error starting ceremony: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error starting ceremony: {e}")
        raise

def record_oath(ceremony_id, heir_id, signature):
    """
    Record an heir's oath during the ceremony.
    
    Args:
        ceremony_id: ID of the active ceremony
        heir_id: Unique identifier for the heir taking the oath
        signature: Digital signature or authentication token
    """
    try:
        payload = {
            "ceremony_id": ceremony_id,
            "heir_id": heir_id,
            "signature": signature,
            "recited_at": datetime.utcnow().isoformat()
        }
        
        print(f"📝 Recording oath for heir {heir_id}")
        r = requests.post(f"{API_URL}/ceremonies/{ceremony_id}/oath", json=payload, headers=HEADERS)
        r.raise_for_status()
        print(f"🕊️ Oath recorded for heir {heir_id} successfully")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error recording oath for heir {heir_id}: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error recording oath: {e}")
        raise

def close_ceremony(ceremony_id):
    """
    Close and archive a ceremony.
    
    Args:
        ceremony_id: ID of the ceremony to close
    
    Returns:
        Dict containing the closed ceremony details
    """
    try:
        print(f"🏁 Closing ceremony {ceremony_id}")
        r = requests.post(f"{API_URL}/ceremonies/{ceremony_id}/close", headers=HEADERS)
        r.raise_for_status()
        ceremony = r.json()
        print(f"✅ Ceremony {ceremony_id} closed and archived at {ceremony['closed_at']}")
        return ceremony
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error closing ceremony: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error closing ceremony: {e}")
        raise

def main():
    """Main ceremony orchestration function."""
    print("🏛️ Codex Induction Ceremony Orchestrator")
    print("=" * 50)
    
    # Validate environment before proceeding
    validate_environment()
    
    try:
        # Step 1: Schedule the ceremony
        print("\n📋 Step 1: Scheduling Induction Ceremony")
        ceremony = schedule_induction()
        cid = ceremony["id"]
        print(f"   Ceremony ID: {cid}")

        # Step 2: Start the ceremony
        print("\n🎭 Step 2: Starting Ceremony")
        start_ceremony(cid)

        # Step 3: Record heir oaths (example heirs)
        print("\n🤝 Step 3: Recording Heir Oaths")
        heirs = [
            {"id": "heir123", "signature": "signature-heir123"},
            {"id": "heir456", "signature": "signature-heir456"},
            {"id": "heir789", "signature": "signature-heir789"}
        ]
        
        for heir in heirs:
            record_oath(cid, heir["id"], heir["signature"])

        # Step 4: Close ceremony
        print("\n🎯 Step 4: Closing Ceremony")
        final_ceremony = close_ceremony(cid)
        
        # Summary
        print("\n" + "=" * 50)
        print("✅ Induction ceremony completed successfully!")
        print(f"📊 Ceremony Summary:")
        print(f"   • ID: {cid}")
        print(f"   • Heirs inducted: {len(heirs)}")
        print(f"   • Closed at: {final_ceremony.get('closed_at', 'Unknown')}")
        print(f"   • Archive status: {final_ceremony.get('status', 'Unknown')}")
            
    except KeyboardInterrupt:
        print("\n⚠️  Ceremony orchestration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ceremony orchestration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()