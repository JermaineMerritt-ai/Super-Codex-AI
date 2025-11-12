from flask import Flask, request, jsonify
import os
import uuid
import datetime
import json
from typing import Dict, Any

app = Flask(__name__)

# Mock ceremonial data storage
ceremonies_db = []
honors_db = []

def generate_dispatch_id() -> str:
    """Generate a unique dispatch ID for ceremonies"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    unique_id = str(uuid.uuid4())[:8]
    return f"AXF-{timestamp}-{unique_id}"

def create_ceremony_entry(actor: str, realm: str, capsule: str, intent: str = None) -> Dict[str, Any]:
    """Create a ceremonial entry with proper structure"""
    dispatch_id = generate_dispatch_id()
    ceremony = {
        "dispatch_id": dispatch_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "actor": actor,
        "realm": realm,
        "capsule": capsule,
        "intent": intent or "General.Invocation",
        "status": "active",
        "governance_seal": "validated",
        "authority_level": "ceremonial",
        "audit_trail": [
            {
                "action": "ceremony_initiated",
                "timestamp": datetime.datetime.now().isoformat(),
                "authority": "AXIOM-Flame"
            }
        ]
    }
    ceremonies_db.append(ceremony)
    return ceremony

@app.route("/execute", methods=["POST"])
def execute():
    """Main execution endpoint for AXIOM commands"""
    try:
        data = request.get_json(force=True) or {}
        command = data.get("command")
        payload = data.get("payload") or {}
        
        if command == "health":
            return jsonify({
                "status": "ok",
                "command": command,
                "result": "AXIOM-Flame operational",
                "ceremonies_count": len(ceremonies_db),
                "honors_count": len(honors_db)
            })
        
        elif command == "reason":
            # Extract ceremonial reasoning parameters from payload
            actor = payload.get("actor", "Unknown")
            realm = payload.get("realm", "UNASSIGNED")
            capsule = payload.get("capsule", "Standard")
            intent = payload.get("intent", "General.Invocation")
            
            ceremony = create_ceremony_entry(actor, realm, capsule, intent)
            
            return jsonify({
                "status": "success",
                "command": command,
                "dispatch_id": ceremony["dispatch_id"],
                "result": "ceremonial_reasoning_complete",
                "ceremony": ceremony
            })
        
        else:
            # Generic command handling
            return jsonify({
                "status": "ok",
                "command": command,
                "result": "ceremony_dispatched",
                "payload": payload
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "command": command if 'command' in locals() else "unknown"
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AXIOM-Flame",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "ceremonies_active": len(ceremonies_db),
        "honors_granted": len(honors_db)
    })

@app.route("/reason", methods=["POST"])
def reason():
    """Ceremonial reasoning endpoint"""
    try:
        data = request.get_json(force=True) or {}
        
        actor = data.get("actor", "Unknown")
        realm = data.get("realm", "UNASSIGNED")
        capsule = data.get("capsule", "Standard")
        intent = data.get("intent", "General.Invocation")
        
        ceremony = create_ceremony_entry(actor, realm, capsule, intent)
        
        return jsonify({
            "status": "success",
            "dispatch_id": ceremony["dispatch_id"],
            "timestamp": ceremony["timestamp"],
            "result": "ceremonial_reasoning_complete",
            "ceremony": {
                "actor": ceremony["actor"],
                "realm": ceremony["realm"],
                "capsule": ceremony["capsule"],
                "intent": ceremony["intent"],
                "status": ceremony["status"]
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route("/grant", methods=["POST"])
def grant():
    """Honor granting endpoint"""
    try:
        data = request.get_json(force=True) or {}
        
        recipient = data.get("recipient", "Unknown")
        honor = data.get("honor", "General Recognition")
        authority = data.get("authority", "AXIOM-Council")
        
        honor_id = f"HK-{len(honors_db) + 1:04d}"
        honor_entry = {
            "honor_id": honor_id,
            "recipient": recipient,
            "honor": honor,
            "authority": authority,
            "granted_at": datetime.datetime.now().isoformat(),
            "status": "active",
            "insignia": f"Distinguished {honor}",
            "seal": "ceremonial_validated"
        }
        
        honors_db.append(honor_entry)
        
        return jsonify({
            "status": "success",
            "honor_id": honor_id,
            "result": "honor_granted",
            "honor": honor_entry
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route("/ceremonies", methods=["GET"])
def ceremonies():
    """List all ceremonial records"""
    return jsonify({
        "status": "success",
        "total": len(ceremonies_db),
        "ceremonies": ceremonies_db[-10:]  # Return last 10 ceremonies
    })

@app.route("/honors", methods=["GET"])
def honors():
    """List all honor records"""
    return jsonify({
        "status": "success",
        "total": len(honors_db),
        "honors": honors_db[-10:]  # Return last 10 honors
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5010))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🔥 Starting AXIOM-Flame on port {port}")
    print(f"📊 Debug mode: {debug}")
    
    app.run(host="127.0.0.1", port=port, debug=debug)