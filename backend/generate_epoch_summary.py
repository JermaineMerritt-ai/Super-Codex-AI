import os
import glob
import re
from datetime import datetime

LOG_DIR = "backend/logs"
SUMMARY_FILE = "backend/logs/capsule_epoch_summary.txt"

# Regex to match log and checksum files
LOG_PATTERN = re.compile(r"capsule_events_(\d{4}-\d{2}-\d{2})\.log$")

# Simulated threat detection (replace with real scanner integration if needed)
def detect_threats(log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()
    if "malicious" in content or "quarantine" in content:
        return ["Finance Capsule quarantine: malicious payload"]
    return ["None detected"]

def verify_checksum(log_path):
    sha_path = log_path + ".sha256"
    if not os.path.exists(sha_path):
        return "FAIL (no checksum)"
    import hashlib
    with open(sha_path, "r") as f:
        line = f.read().strip()
        expected_hash, filename = line.split("  ")
    with open(log_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    return "PASS" if actual_hash == expected_hash else "FAIL"

def generate_epoch_summary():
    logs = glob.glob(os.path.join(LOG_DIR, "capsule_events_*.log"))
    epochs = {}
    for log in logs:
        m = LOG_PATTERN.search(os.path.basename(log))
        if not m:
            continue
        date = m.group(1)
        if date not in epochs:
            epochs[date] = {"logs": [], "threats": [], "verification": []}
        epochs[date]["logs"].append(os.path.basename(log))
        sha_file = os.path.basename(log) + ".sha256"
        if os.path.exists(os.path.join(LOG_DIR, sha_file)):
            epochs[date]["logs"].append(sha_file)
        # Threats
        threats = detect_threats(log)
        epochs[date]["threats"].extend(threats)
        # Verification
        result = verify_checksum(log)
        epochs[date]["verification"].append(f"{os.path.basename(log)}: {result}")
    # Write summary
    with open(SUMMARY_FILE, "w") as f:
        for date in sorted(epochs.keys()):
            f.write(f"Epoch: {date}\n")
            f.write("  Logs:\n")
            for logf in epochs[date]["logs"]:
                f.write(f"    - {logf}\n")
            f.write("  Threats:\n")
            for threat in set(epochs[date]["threats"]):
                f.write(f"    - {threat}\n")
            f.write("  Verification:\n")
            for v in epochs[date]["verification"]:
                f.write(f"    - {v}\n")
            f.write("\n")
    print(f"Summary written to {SUMMARY_FILE}")

if __name__ == "__main__":
    generate_epoch_summary()
