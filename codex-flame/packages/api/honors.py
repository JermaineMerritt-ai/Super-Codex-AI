from flask import Blueprint, request, jsonify
from pathlib import Path
import json, uuid, datetime

bp = Blueprint("honors", __name__)
BASE = Path(__file__).resolve().parents[2]
STORAGE = BASE / "storage"
HONORS = STORAGE / "honors"
TRANSMIT = STORAGE / "transmissions"
REPLAYS = STORAGE / "replays"

for p in [HONORS, TRANSMIT, REPLAYS]:
    p.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

@bp.post("/honors")
def inscribe_honor():
    payload = request.get_json(force=True)
    honor_id = f"HON-{str(uuid.uuid4())[:8]}"
    entry = {
        "schema": "honors.v1",
        "honor_id": honor_id,
        "timestamp": now_iso(),
        "name": payload.get("name"),
        "deed": payload.get("deed"),
        "realm": payload.get("realm","Planetary"),
        "seal": payload.get("seal","Eternal"),
        "links": {"dispatch_id": payload.get("dispatch_id")}
    }
    (HONORS / f"{honor_id}.json").write_text(json.dumps(entry, indent=2), encoding="utf-8")
    return jsonify({"ok": True, "honor_id": honor_id, "entry": entry})

@bp.post("/transmit/honors")
def transmit_honors():
    payload = request.get_json(force=True)
    honors_list = payload.get("honors", [])
    broadcast_id = f"TX-HON-{str(uuid.uuid4())[:8]}"
    artifact = {
        "schema": "transmit.honors.v1",
        "broadcast_id": broadcast_id,
        "timestamp": now_iso(),
        "council": payload.get("council","Dominion"),
        "honors": honors_list,
        "audit": {"status":"Broadcast", "sealed": True}
    }
    (TRANSMIT / f"{broadcast_id}.json").write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    # create replay capsule so councils can recall the proclamation
    replay_id = f"RP-{str(uuid.uuid4())[:8]}"
    replay = {
        "schema": "replay.v1",
        "replay_id": replay_id,
        "timestamp": now_iso(),
        "source_broadcast_id": broadcast_id,
        "intent": "Honors.Broadcast",
        "summary": f"{len(honors_list)} honors proclaimed"
    }
    (REPLAYS / f"{replay_id}.json").write_text(json.dumps(replay, indent=2), encoding="utf-8")

    artifact["replay_id"] = replay_id
    return jsonify({"ok": True, "broadcast_id": broadcast_id, "replay_id": replay_id})