#!/usr/bin/env python3
"""
Generate monthly annals from ledger entries.

This script processes all ledger entries and groups them by month,
creating summary files in the annals directory for historical tracking.
"""

from pathlib import Path
import json, datetime

BASE = Path(__file__).resolve().parents[1]
LEDGER = BASE / "storage" / "ledger"
CEREMONIES = BASE / "artifacts" / "ceremonies"
ANNALS = BASE / "storage" / "annals"

def month_key(dt):
    """Generate a month key in YYYY-MM format."""
    return f"{dt.year}-{dt.month:02d}"

def run():
    """Process ledger entries and ceremony files to generate monthly annals."""
    # Ensure annals directory exists
    ANNALS.mkdir(parents=True, exist_ok=True)
    
    groups = {}
    
    # Process all ledger files
    if LEDGER.exists():
        for f in LEDGER.glob("*.json"):
            process_file(f, groups, "ledger")
    
    # Process all ceremony files
    if CEREMONIES.exists():
        for f in CEREMONIES.glob("*.json"):
            process_file(f, groups, "ceremony")

def process_file(f, groups, file_type):
    """Process a single JSON file and add to groups."""
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        
        # Handle nested ledger entry structure
        if "ledger_entry" in data:
            entry = data["ledger_entry"]
            ts = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z",""))
            key = month_key(ts)
            
            groups.setdefault(key, []).append({
                "dispatch_id": entry["dispatch_id"],
                "timestamp": entry["timestamp"],
                "status": entry.get("status", "unknown"),
                "type": "ledger"
            })
        else:
            # Handle direct entry structure (ceremony entries)
            entry = data
            ts = datetime.datetime.fromisoformat(entry["timestamp"].replace("Z",""))
            key = month_key(ts)
            
            groups.setdefault(key, []).append({
                "dispatch_id": entry["dispatch_id"],
                "realm": entry.get("realm", "unknown"),
                "capsule": entry.get("capsule", "unknown"),
                "intent": entry.get("intent", "unknown"),
                "summary": entry.get("output", {}).get("summary", "No summary available"),
                "type": "ceremony"
            })
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Skipping invalid {file_type} file {f.name}: {e}")
    
    # Write monthly annals
    for k, items in groups.items():
        out = ANNALS / f"{k}.json"
        annal_data = {
            "month": k,
            "total_entries": len(items),
            "generated_at": datetime.datetime.now().isoformat(),
            "entries": items
        }
        out.write_text(json.dumps(annal_data, indent=2), encoding="utf-8")
        print(f"Generated annal for {k}: {len(items)} entries")
    
    print(f"Processing complete. Generated {len(groups)} monthly annals.")

if __name__ == "__main__":
    run()