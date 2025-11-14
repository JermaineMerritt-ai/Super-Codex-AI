import os
from app.config import settings

def save_replay_capsule(capsule_bytes, name: str):
    path = os.path.join(settings.REPLAY_ARCHIVE_PATH, f"{name}.zip")
    with open(path, "wb") as f:
        f.write(capsule_bytes)
    return path

def append_audit_log(entry: str):
    with open(settings.AUDIT_LOG_PATH, "a") as f:
        f.write(entry + "\n")