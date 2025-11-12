# millennial_rite.py
# Binds Great Year proclamations into the Eternal Continuum
from pathlib import Path
import json, datetime, uuid

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"
GREATYEAR = STORAGE / "greatyear"
MILLENNIAL = STORAGE / "millennial"
MILLENNIAL.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def continuum_binding():
    proclamations = []
    for f in GREATYEAR.glob("*.json"):
        entry = json.loads(f.read_text(encoding="utf-8"))
        proclamations.append({
            "proclamation_id": entry["proclamation_id"],
            "epoch": entry["epoch"],
            "summary": entry["summary"]
        })

    rite_id = f"MILL-{str(uuid.uuid4())[:8]}"
    capsule = {
        "schema": "millennial.v1",
        "rite_id": rite_id,
        "timestamp": now_iso(),
        "epochs_bound": len(proclamations),
        "continuum": proclamations,
        "summary": f"Millennial Rite: {len(proclamations)} epochs bound into Eternal Continuum."
    }

    (MILLENNIAL / f"{rite_id}.json").write_text(json.dumps(capsule, indent=2), encoding="utf-8")
    print(f"[MILLENNIAL] {capsule['summary']}")

if __name__ == "__main__":
    continuum_binding()