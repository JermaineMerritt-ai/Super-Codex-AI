from pathlib import Path
import json, datetime

BASE = Path(__file__).resolve().parents[1]
LEDGER = BASE / "storage" / "ledger"
ANNALS = BASE / "storage" / "annals"

def month_key(dt):
    return f"{dt.year}-{dt.month:02d}"

def run():
    ANNALS.mkdir(parents=True, exist_ok=True)
    groups = {}
    for f in LEDGER.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        
        # Handle nested legacy format
        if "ledger_entry" in data:
            entry = data["ledger_entry"]
            ts = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z",""))
            key = month_key(ts)
            groups.setdefault(key, []).append({
                "dispatch_id": entry["dispatch_id"],
                "timestamp": entry["timestamp"],
                "status": entry.get("status", "unknown")
            })
        else:
            # Handle new direct format
            entry = data
            ts = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z",""))
            key = month_key(ts)
            groups.setdefault(key, []).append({
                "dispatch_id": entry["dispatch_id"],
                "realm": entry["realm"],
                "capsule": entry["capsule"],
                "intent": entry["intent"],
                "summary": entry["output"]["summary"]
            })
    
    for k, items in groups.items():
        out = ANNALS / f"{k}.json"
        out.write_text(json.dumps({"month": k, "entries": items}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    run()