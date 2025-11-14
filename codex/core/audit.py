import orjson
from pathlib import Path
from time import time
from .config import settings

def log_event(event_type: str, payload: dict) -> dict:
    record = {"ts": time(), "type": event_type, "payload": payload}
    Path(settings.AUDIT_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(settings.AUDIT_LOG_PATH, "ab") as f:
        f.write(orjson.dumps(record) + b"\n")
    return record