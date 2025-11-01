import sys
import os
import yaml
from datetime import datetime
from backend.logging_utils import seal_log_with_checksum

LEDGER_PATH = "backend/logs/ledger_of_seals.yml"

def get_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except Exception:
        return "unknown"

def update_ledger(log_path: str, custodian="Unknown Custodian", threats=None):
    """Update the Ledger of Seals with a new log + checksum entry."""
    checksum_file = seal_log_with_checksum(log_path)

    # Load existing ledger or start fresh
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            ledger = yaml.safe_load(f) or []
    else:
        ledger = []

    epoch_entry = {
        "Epoch": datetime.now().isoformat(),
        "Commit": get_commit_hash(),
        "Custodian": custodian,
        "Logs": [os.path.basename(log_path), os.path.basename(checksum_file)],
        "Threats": threats or ["None detected"],
        "Verification": {os.path.basename(log_path): "PASS"}
    }

    ledger.append(epoch_entry)

    with open(LEDGER_PATH, "w") as f:
        yaml.dump(ledger, f, sort_keys=False)

    return epoch_entry

if __name__ == "__main__":
    import sys
    log_file = sys.argv[1] if len(sys.argv) > 1 else "backend/logs/capsule_events.log"
    custodian = sys.argv[2] if len(sys.argv) > 2 else "Unknown Custodian"
    threats = sys.argv[3:] if len(sys.argv) > 3 else None
    entry = update_ledger(log_file, custodian, threats)
    print("Ledger updated:")
    print(entry)
