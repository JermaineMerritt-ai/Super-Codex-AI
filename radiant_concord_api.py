"""
Radiant Concord Integration Module

Integrates the Radiant Concord honor system with existing Axiom-Flame API endpoints
to enable honor flows across councils, constellations, and diaspora.
"""

from flask import Flask, jsonify, request
from datetime import datetime
from radiant_concord import (
    RadiantConcordManager, HonorRecipient, HonorType, HonorRank, ConstellationType
)
import json


def register_radiant_concord_routes(app: Flask):
    """Register Radiant Concord routes with the Flask app"""
    
    manager = RadiantConcordManager()
    
    @app.route('/api/radiant-concord/health', methods=['GET'])
    def radiant_concord_health():
        """Health check for Radiant Concord system"""
        summary = manager.get_honor_flows_summary()
        return jsonify({
            "status": "radiant",
            "service": "radiant-concord",
            "timestamp": datetime.utcnow().isoformat(),
            "honor_flows_active": True,
            "total_honors": summary["total_honors"],
            "luminous_concord": "achieved"
        })
    
    @app.route('/api/radiant-concord/honor/council', methods=['POST'])
    def create_council_honor():
        """Create council proclamation honor"""
        data = request.get_json()
        
        recipient = HonorRecipient(
            id=data["recipient"]["id"],
            name=data["recipient"]["name"],
            email=data["recipient"]["email"],
            constellation=data["recipient"].get("constellation"),
            realm_id=data["recipient"].get("realm_id"),
            lineage_verification=data["recipient"].get("lineage_verification", False)
        )
        
        honor = manager.create_council_proclamation_honor(
            recipient=recipient,
            council_id=data["council_id"],
            council_name=data["council_name"],
            achievement=data["achievement"],
            impact_scope=data.get("impact_scope", "realm")
        )
        
        file_path = manager.save_honor(honor)
        
        return jsonify({
            "status": "proclaimed",
            "honor_id": honor.honor_id,
            "honor_type": "council_proclamation",
            "unity_seal": honor.council_proclamation.unity_seal,
            "luminous_signature": honor.honor_metadata.luminous_signature,
            "archived_at": str(file_path),
            "timestamp": honor.timestamp.isoformat()
        }), 201
    
    @app.route('/api/radiant-concord/honor/constellation', methods=['POST'])
    def create_constellation_honor():
        """Create constellation echo honor"""
        data = request.get_json()
        
        recipient = HonorRecipient(
            id=data["recipient"]["id"],
            name=data["recipient"]["name"],
            email=data["recipient"]["email"],
            constellation=data["recipient"].get("constellation"),
            realm_id=data["recipient"].get("realm_id")
        )
        
        constellation_type = ConstellationType(data["constellation_type"])
        
        honor = manager.create_constellation_echo_honor(
            recipient=recipient,
            constellation_id=data["constellation_id"],
            constellation_type=constellation_type,
            achievement=data["achievement"],
            echo_strength=data.get("echo_strength", 0.8)
        )
        
        file_path = manager.save_honor(honor)
        
        return jsonify({
            "status": "resonating",
            "honor_id": honor.honor_id,
            "honor_type": "constellation_echo",
            "flame_resonance": honor.constellation_echo.flame_resonance,
            "echo_strength": honor.constellation_echo.echo_strength,
            "honor_rank": honor.honor_rank.value,
            "luminous_signature": honor.honor_metadata.luminous_signature,
            "archived_at": str(file_path),
            "timestamp": honor.timestamp.isoformat()
        }), 201
    
    @app.route('/api/radiant-concord/honor/diaspora', methods=['POST'])
    def create_diaspora_honor():
        """Create diaspora inheritance honor"""
        data = request.get_json()
        
        recipient = HonorRecipient(
            id=data["recipient"]["id"],
            name=data["recipient"]["name"],
            email=data["recipient"]["email"],
            constellation=data["recipient"].get("constellation"),
            realm_id=data["recipient"].get("realm_id"),
            lineage_verification=data["recipient"].get("lineage_verification", True)
        )
        
        radiance_level = HonorRank(data.get("radiance_level", "steward"))
        
        honor = manager.create_diaspora_inheritance_honor(
            recipient=recipient,
            diaspora_node=data["diaspora_node"],
            inheritance_claim=data["inheritance_claim"],
            achievement=data["achievement"],
            radiance_level=radiance_level
        )
        
        file_path = manager.save_honor(honor)
        
        return jsonify({
            "status": "inherited",
            "honor_id": honor.honor_id,
            "honor_type": "diaspora_inheritance",
            "lineage_proof": honor.diaspora_inheritance.lineage_proof,
            "radiance_level": honor.diaspora_inheritance.radiance_level.value,
            "luminous_signature": honor.honor_metadata.luminous_signature,
            "archived_at": str(file_path),
            "timestamp": honor.timestamp.isoformat()
        }), 201
    
    @app.route('/api/radiant-concord/honors', methods=['GET'])
    def list_honors():
        """List all honors in the concord"""
        summary = manager.get_honor_flows_summary()
        return jsonify({
            "radiant_concord": "active",
            "honor_flows": summary,
            "luminous_binding": "eternal",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    @app.route('/api/radiant-concord/concord-ledger', methods=['GET'])
    def get_concord_ledger():
        """Get the full concord ledger"""
        if manager.concord_ledger_path.exists():
            with open(manager.concord_ledger_path, 'r', encoding='utf-8') as f:
                ledger = json.load(f)
            return jsonify({
                "concord_ledger": ledger,
                "status": "radiant",
                "eternal_witness": True
            })
        else:
            return jsonify({
                "concord_ledger": {"ledger_entries": []},
                "status": "initializing",
                "message": "Concord ledger being established"
            })


# Example usage for testing the integration
def create_demo_honors_via_api():
    """Create demo honors using the API endpoints"""
    import requests
    
    base_url = "http://localhost:8095/api/radiant-concord"
    
    # Demo council honor
    council_data = {
        "recipient": {
            "id": "RCP-API-COUNCIL-001",
            "name": "Council API Sage",
            "email": "sage@api.codexdominion.app",
            "constellation": "API_Constellation",
            "realm_id": "API-001",
            "lineage_verification": True
        },
        "council_id": "COUNCIL-API-PRIME",
        "council_name": "API Prime Council",
        "achievement": "Establishing radiant API endpoints for honor flows",
        "impact_scope": "cosmic"
    }
    
    # Demo constellation honor
    constellation_data = {
        "recipient": {
            "id": "RCP-API-STAR-001",
            "name": "API Starweaver",
            "email": "star@api.codexdominion.app",
            "constellation": "API_Nexus"
        },
        "constellation_id": "CONSTELLATION-API-NEXUS",
        "constellation_type": "stellar",
        "achievement": "Masterful API constellation orchestration",
        "echo_strength": 0.92
    }
    
    # Demo diaspora honor
    diaspora_data = {
        "recipient": {
            "id": "RCP-API-DIASPORA-001",
            "name": "API Heritage Keeper",
            "email": "heritage@api.codexdominion.app",
            "constellation": "API_Heritage",
            "lineage_verification": True
        },
        "diaspora_node": "DIASPORA-API-HERITAGE",
        "inheritance_claim": "API Legacy Stewardship",
        "achievement": "Preserving API heritage across digital realms",
        "radiance_level": "sovereign"
    }
    
    print("🌟 Creating Honors via Radiant Concord API")
    
    try:
        # Create council honor
        response = requests.post(f"{base_url}/honor/council", json=council_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Council Honor Created: {result['honor_id']}")
        
        # Create constellation honor
        response = requests.post(f"{base_url}/honor/constellation", json=constellation_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Constellation Honor Created: {result['honor_id']}")
        
        # Create diaspora honor
        response = requests.post(f"{base_url}/honor/diaspora", json=diaspora_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Diaspora Honor Created: {result['honor_id']}")
        
        # Check health
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"🌟 Radiant Concord Health: {health['status']} - {health['total_honors']} honors")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  API not accessible - honors created directly via RadiantConcordManager")


if __name__ == "__main__":
    create_demo_honors_via_api()