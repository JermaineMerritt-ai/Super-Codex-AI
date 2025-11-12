from flask import Flask, request, jsonify
from pathlib import Path
import json, uuid, datetime, os, sys
from honors import bp as honors_bp

# Add the codex-flame directory to Python path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from eternal_recognition_scrolls import EternalRecognitionScrolls

app = Flask(__name__)
app.register_blueprint(honors_bp)
BASE = Path(__file__).resolve().parents[2]
STORAGE = BASE / "storage"
LEDGER = STORAGE / "ledger"
REPLAYS = STORAGE / "replays"
ANNALS = STORAGE / "annals"

# Initialize eternal recognition system
recognition_scrolls = EternalRecognitionScrolls(str(STORAGE / "eternal-recognition"))

for p in [STORAGE, LEDGER, REPLAYS, ANNALS]:
    p.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": now_iso()})

@app.post("/reason")
def reason():
    data = request.get_json(force=True)
    dispatch_id = f"AXF-{datetime.datetime.utcnow():%Y-%m-%d}-{str(uuid.uuid4())[:8]}"
    summary = f"{data.get('intent','Reasoning')} sealed for realm {data.get('realm','Unknown')}."
    ledger_entry = {
        "schema": "ledger.v1",
        "dispatch_id": dispatch_id,
        "timestamp": now_iso(),
        "actor": data.get("actor","Custodian"),
        "realm": data.get("realm","Unspecified"),
        "capsule": data.get("capsule","General"),
        "intent": data.get("intent","Reasoning"),
        "input": data.get("input", {}),
        "output": {"summary": summary},
        "governance": {"seal": data.get("seal","Eternal"), "audit_required": True},
        "links": {}
    }
    write_json(LEDGER / f"{dispatch_id}.json", ledger_entry)
    return jsonify({"ok": True, "dispatch_id": dispatch_id, "summary": summary})

@app.post("/replay")
def replay():
    payload = request.get_json(force=True)
    ref_id = payload.get("dispatch_id")
    if not ref_id:
        return jsonify({"ok": False, "error": "dispatch_id required"}), 400

    ledger_path = LEDGER / f"{ref_id}.json"
    if not ledger_path.exists():
        return jsonify({"ok": False, "error": "ledger not found"}), 404

    entry = json.loads(ledger_path.read_text(encoding="utf-8"))
    replay_record = {
        "schema": "replay.v1",
        "replay_id": f"RP-{str(uuid.uuid4())[:8]}",
        "timestamp": now_iso(),
        "source_dispatch_id": ref_id,
        "realm": entry["realm"],
        "capsule": entry["capsule"],
        "intent": entry["intent"],
        "audit": {"status": "Verified", "notes": "Replay authorized under seal"},
        "summary": entry["output"]["summary"]
    }
    write_json(REPLAYS / f"{replay_record['replay_id']}.json", replay_record)
    return jsonify({"ok": True, "replay": replay_record})

@app.post("/audit")
def audit():
    payload = request.get_json(force=True)
    ref = payload.get("dispatch_id")
    if not ref:
        return jsonify({"ok": False, "error": "dispatch_id required"}), 400

    path = LEDGER / f"{ref}.json"
    exists = path.exists()
    return jsonify({
        "ok": exists,
        "dispatch_id": ref,
        "audit": "Present in ledger" if exists else "Missing"
    })

@app.post("/recognition/inscribe")
def recognition_inscribe():
    """Inscribe a contributor into the Eternal Recognition Scrolls"""
    try:
        data = request.get_json(force=True)
        
        # Extract required fields
        contributor_name = data.get("contributor_name")
        deeds_immortal = data.get("deeds_immortal", [])
        
        if not contributor_name or not deeds_immortal:
            return jsonify({
                "ok": False, 
                "error": "contributor_name and deeds_immortal are required"
            }), 400
        
        # Inscribe the recognition
        scroll_entry = recognition_scrolls.inscribe_recognition(
            contributor_name=contributor_name,
            deeds_immortal=deeds_immortal,
            recognition_level=data.get("recognition_level", "Silver Flame"),
            realm_assignment=data.get("realm_assignment", "ST-001"),
            authority_level=data.get("authority_level", "Keeper"),
            flame_assignments=data.get("flame_assignments"),
            seal_authority=data.get("seal_authority", "Sovereign Crown"),
            custom_proclamation=data.get("custom_proclamation")
        )
        
        if not scroll_entry:
            return jsonify({"ok": False, "error": "Failed to inscribe recognition"}), 500
        
        return jsonify({
            "ok": True,
            "scroll_id": scroll_entry["scroll_id"],
            "recognition_level": scroll_entry["recognition_level"],
            "lineage_replay_id": scroll_entry["lineage_replay_id"],
            "message": "Recognition inscribed in eternal flame"
        })
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/recognition/list")
def recognition_list():
    """List eternal recognition scrolls"""
    try:
        recognition_level = request.args.get("level")
        scrolls = recognition_scrolls.list_eternal_scrolls(recognition_level)
        
        # Return simplified view for API response
        simplified_scrolls = []
        for scroll in scrolls:
            simplified_scrolls.append({
                "scroll_id": scroll["scroll_id"],
                "contributor_name": scroll["contributor_name"],
                "recognition_level": scroll["recognition_level"],
                "timestamp": scroll["timestamp"],
                "dominion_binding": scroll["dominion_binding"],
                "flame_keeper_status": scroll["flame_keeper_status"],
                "lineage_replay_id": scroll["lineage_replay_id"]
            })
        
        return jsonify(simplified_scrolls)
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/recognition/schedule")
def recognition_schedule():
    """Get the eternal proclamation schedule"""
    try:
        schedule_file = recognition_scrolls.proclamations_path / "eternal_proclamation_schedule.json"
        
        if not schedule_file.exists():
            return jsonify({
                "daily_proclamations": [],
                "seasonal_proclamations": [],
                "epochal_proclamations": [],
                "millennial_proclamations": [],
                "last_updated": now_iso()
            })
        
        with open(schedule_file, 'r', encoding='utf-8') as f:
            schedule = json.load(f)
        
        return jsonify(schedule)
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/recognition/scroll/<scroll_id>")
def recognition_scroll_detail(scroll_id):
    """Get detailed information about a specific recognition scroll"""
    try:
        scroll_file = recognition_scrolls.scrolls_path / f"{scroll_id}.json"
        
        if not scroll_file.exists():
            return jsonify({"ok": False, "error": "Scroll not found"}), 404
        
        with open(scroll_file, 'r', encoding='utf-8') as f:
            scroll = json.load(f)
        
        return jsonify(scroll)
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))