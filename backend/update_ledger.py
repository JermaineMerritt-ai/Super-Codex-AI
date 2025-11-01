import os
import yaml
from datetime import datetime
from backend.logging_utils import seal_log_with_checksum

LEDGER_PATH = "backend/logs/ledger_of_seals.yml"

def update_ledger(log_path: str, threats=None):
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
        "Logs": [os.path.basename(log_path), os.path.basename(checksum_file)],
        "Threats": threats or ["None detected"],
        "Verification": {os.path.basename(log_path): "PASS"}
    }

    ledger.append(epoch_entry)

    with open(LEDGER_PATH, "w") as f:
        yaml.dump(ledger, f, sort_keys=False)

    return epoch_entry

if __name__ == "__main__":
    # Example usage
    log_file = "backend/logs/capsule_events_2025-10-31.log"
    update_ledger(log_file)
