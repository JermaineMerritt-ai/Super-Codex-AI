import logging
from logging.handlers import TimedRotatingFileHandler
import os
import hashlib

LOG_DIR = "backend/logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "capsule_events.log")

logger = logging.getLogger("CodexCapsule")
logger.setLevel(logging.INFO)



class ChecksumTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        seal_log_with_checksum(self.baseFilename)

# Rotate daily at midnight, keep 30 days of logs
handler = ChecksumTimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=30, utc=True
)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_capsule_event(message: str):
    logger.info(message)

def seal_log_with_checksum(log_path: str):
    """Generate SHA256 checksum for a sealed log scroll, compatible with sha256sum -c."""
    sha256 = hashlib.sha256()
    with open(log_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    checksum = sha256.hexdigest()

    checksum_path = log_path + ".sha256"
    with open(checksum_path, "w") as f:
        # Format: <hash><two spaces><filename>
        f.write(f"{checksum}  {os.path.basename(log_path)}\n")

    return checksum_path
