#!/usr/bin/env python3
"""
Axiom-flame API Service
Ceremonial operations and governance API for CodexDominion.app
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import uuid
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)
CORS(app)  # Allow all origins for development

# Mock Data
REALMS = {
    "PL-001": {"name": "Primary Legion", "status": "active", "capsules": ["Sovereign Crown", "Battle Standard"]},
    "ST-007": {"name": "Strategic Command", "status": "active", "capsules": ["Command Scepter", "War Banner"]},
    "RC-003": {"name": "Reconnaissance Unit", "status": "standby", "capsules": ["Scout Badge", "Field Manual"]}
}

REGISTRY = {
    "actors": ["Custodian", "Marshal", "Sentinel", "Scribe"],
    "realms": list(REALMS.keys()),
    "capsules": {
        "PL-001": ["Sovereign Crown", "Battle Standard"],
        "ST-007": ["Command Scepter", "War Banner"], 
        "RC-003": ["Scout Badge", "Field Manual"]
    },
    "intents": ["Crown.Invocation", "Banner.Ceremony", "Scepter.Command", "Badge.Recognition"]
}

CEREMONIES = []

# Helper Functions
def generate_dispatch_id():
    """Generate unique dispatch ID for ceremonies"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"AXF-{timestamp}-{str(uuid.uuid4())[:8].upper()}"

def validate_ceremony_params(params):
    """Validate ceremony parameters against registry"""
    errors = []
    
    if params.get("actor") not in REGISTRY["actors"]:
        errors.append(f"Invalid actor: {params.get('actor')}")
    
    if params.get("realm") not in REGISTRY["realms"]:
        errors.append(f"Invalid realm: {params.get('realm')}")
    
    realm = params.get("realm")
    capsule = params.get("capsule")
    if realm and capsule and capsule not in REGISTRY["capsules"].get(realm, []):
        errors.append(f"Capsule '{capsule}' not available in realm '{realm}'")
    
    return errors

# Health Endpoint
@app.route("/health", methods=["GET"])
def health():
    """Health check for axiom-flame service"""
    return jsonify({
        "status": "healthy",
        "service": "axiom-flame",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "registry": {
            "realms": len(REALMS),
            "actors": len(REGISTRY["actors"]),
            "ceremonies": len(CEREMONIES)
        }
    })

# Ceremony Operations
@app.route("/reason", methods=["POST"])
def invoke_ceremony():
    """Invoke ceremonial reasoning operation"""
    try:
        params = request.get_json()
        
        # Validate required parameters
        required = ["actor", "realm", "capsule"]
        missing = [field for field in required if not params.get(field)]
        if missing:
            return jsonify({
                "error": "Missing required parameters",
                "missing": missing
            }), 400
        
        # Validate parameters against registry
        validation_errors = validate_ceremony_params(params)
        if validation_errors:
            return jsonify({
                "error": "Validation failed",
                "details": validation_errors
            }), 400
        
        # Create ceremony record
        dispatch_id = generate_dispatch_id()
        ceremony = {
            "dispatch_id": dispatch_id,
            "status": "invoked",
            "timestamp": datetime.datetime.now().isoformat(),
            "actor": params["actor"],
            "realm": params["realm"],
            "capsule": params["capsule"],
            "intent": params.get("intent", "General.Operation"),
            "metadata": {
                "invocation_method": "ceremonial_reasoning",
                "authority_level": "sovereign",
                "governance_seal": f"SEAL-{dispatch_id[:8]}"
            }
        }
        
        CEREMONIES.append(ceremony)
        logger.info(f"Ceremony invoked: {dispatch_id} by {params['actor']} in {params['realm']}")
        
        return jsonify(ceremony)
        
    except Exception as e:
        logger.error(f"Ceremony invocation failed: {str(e)}")
        return jsonify({
            "error": "Ceremony invocation failed",
            "details": str(e)
        }), 500

# Registry Operations
@app.route("/realms", methods=["GET"])
def get_realms():
    """Get available realms"""
    return jsonify({
        "realms": REALMS,
        "count": len(REALMS),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/registry", methods=["GET"])
def get_registry():
    """Get complete registry information"""
    return jsonify({
        "registry": REGISTRY,
        "metadata": {
            "last_updated": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "total_entities": sum(len(v) if isinstance(v, list) else len(v) for v in REGISTRY.values())
        }
    })

# Ceremony History
@app.route("/ceremonies", methods=["GET"])
def get_ceremonies():
    """Get ceremony history"""
    return jsonify({
        "ceremonies": CEREMONIES,
        "count": len(CEREMONIES),
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/ceremonies/<dispatch_id>", methods=["GET"])
def get_ceremony(dispatch_id):
    """Get specific ceremony by dispatch ID"""
    ceremony = next((c for c in CEREMONIES if c["dispatch_id"] == dispatch_id), None)
    if not ceremony:
        return jsonify({"error": "Ceremony not found"}), 404
    
    return jsonify(ceremony)

# Root endpoint
@app.route("/", methods=["GET"])
def root():
    """Root endpoint with service information"""
    return jsonify({
        "service": "Axiom-flame Ceremonial API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "reason": "/reason",
            "realms": "/realms", 
            "registry": "/registry",
            "ceremonies": "/ceremonies"
        },
        "timestamp": datetime.datetime.now().isoformat(),
        "motto": "Per Axioma ad Astra - Through Axioms to the Stars"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested API endpoint does not exist",
        "available_endpoints": ["/", "/health", "/reason", "/realms", "/registry", "/ceremonies"],
        "timestamp": datetime.datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error", 
        "message": str(error),
        "timestamp": datetime.datetime.now().isoformat()
    }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5010))
    print(f"Starting Axiom-flame API on http://127.0.0.1:{port}")
    print("Available endpoints:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    
    app.run(host="127.0.0.1", port=port, debug=True)