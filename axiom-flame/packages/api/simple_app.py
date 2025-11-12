from flask import Flask, jsonify, request
import datetime
import json

app = Flask(__name__)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

@app.route("/")
def root():
    return "Axiom-Flame Ceremonial API - Ready for Governance"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": now_iso()})

@app.route("/reason", methods=["POST"])
def reason():
    data = request.get_json(force=True)
    dispatch_id = f"AXF-{datetime.datetime.utcnow():%Y-%m-%d}-{hash(str(data))%100000000:08d}"
    summary = f"{data.get('intent','Reasoning')} sealed for realm {data.get('realm','Unknown')}."
    
    return jsonify({
        "ok": True, 
        "dispatch_id": dispatch_id, 
        "summary": summary,
        "actor": data.get("actor", "Custodian"),
        "realm": data.get("realm", "Unspecified"),
        "capsule": data.get("capsule", "General")
    })

@app.route("/replay", methods=["POST"])
def replay():
    payload = request.get_json(force=True)
    dispatch_id = payload.get("dispatch_id")
    
    if not dispatch_id:
        return jsonify({"ok": False, "error": "dispatch_id required"}), 400
    
    replay_record = {
        "replay_id": f"RP-{hash(dispatch_id)%100000000:08d}",
        "timestamp": now_iso(),
        "source_dispatch_id": dispatch_id,
        "realm": "Test-Realm",
        "capsule": "Test-Capsule",
        "audit": {"status": "Verified", "notes": "Replay authorization matched Eternal Seal"}
    }
    
    return jsonify({"ok": True, "replay": replay_record})

@app.route("/audit", methods=["POST"])
def audit():
    payload = request.get_json(force=True)
    dispatch_id = payload.get("dispatch_id")
    
    if not dispatch_id:
        return jsonify({"ok": False, "error": "dispatch_id required"}), 400
    
    # For testing, assume all dispatch IDs exist
    return jsonify({
        "ok": True,
        "dispatch_id": dispatch_id,
        "audit": "Present in ledger"
    })

if __name__ == "__main__":
    print("Starting Axiom-Flame API...")
    app.run(host="127.0.0.1", port=8081, debug=True)