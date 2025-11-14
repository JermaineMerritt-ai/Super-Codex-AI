#!/usr/bin/env python3
import os
import json
import zipfile
from datetime import datetime, timezone

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./data/audit.log")
LEDGER_PATH = os.getenv("LEDGER_PATH", "./storage/ledger")
ANNALS_PATH = os.getenv("ANNALS_PATH", "./storage/annals")
REPLAYS_PATH = os.getenv("REPLAYS_PATH", "./storage/replays")

def generate_capsule(name="replay_capsule"):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    capsule_name = f"{name}_{timestamp}.zip"
    capsule_path = os.path.join(REPLAYS_PATH, capsule_name)

    os.makedirs(REPLAYS_PATH, exist_ok=True)

    with zipfile.ZipFile(capsule_path, "w", zipfile.ZIP_DEFLATED) as capsule:
        # Include audit log
        if os.path.exists(AUDIT_LOG_PATH):
            capsule.write(AUDIT_LOG_PATH, arcname="audit.log")

        # Include ledger
        if os.path.exists(LEDGER_PATH):
            for root, _, files in os.walk(LEDGER_PATH):
                for f in files:
                    capsule.write(os.path.join(root, f), arcname=f"ledger/{f}")

        # Include annals
        if os.path.exists(ANNALS_PATH):
            for root, _, files in os.walk(ANNALS_PATH):
                for f in files:
                    capsule.write(os.path.join(root, f), arcname=f"annals/{f}")

    print(f"✅ Replay capsule generated: {capsule_path}")
    return capsule_path

if __name__ == "__main__":
    generate_capsule("codex_replay")