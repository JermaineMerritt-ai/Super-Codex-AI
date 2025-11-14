import orjson
from pathlib import Path
from time import time
from .config import settings

def archive(tag: str, data: dict) -> str:
    Path(settings.REPLAY_DIR).mkdir(parents=True, exist_ok=True)
    path = Path(settings.REPLAY_DIR) / f"{int(time())}-{tag}.json"
    with open(path, "wb") as f:
        f.write(orjson.dumps(data))
    return str(path)