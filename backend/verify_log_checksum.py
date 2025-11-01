import hashlib
import os

def verify_log_checksum(log_path: str):
    checksum_path = log_path + ".sha256"
    if not os.path.exists(checksum_path):
        print("Checksum file not found.")
        return False
    with open(checksum_path, "r") as f:
        line = f.read().strip()
        expected_hash, filename = line.split("  ")
    with open(log_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    if actual_hash == expected_hash:
        print("OK")
        return True
    else:
        print("FAILED")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python verify_log_checksum.py <log_file_path>")
        exit(1)
    verify_log_checksum(sys.argv[1])
