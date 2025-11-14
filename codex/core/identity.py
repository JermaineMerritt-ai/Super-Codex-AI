import orjson
from pathlib import Path
from .config import settings

def save_identity(slug: str, data: dict) -> str:
    Path(settings.IDENTITIES_DIR).mkdir(parents=True, exist_ok=True)
    path = Path(settings.IDENTITIES_DIR) / f"{slug}.json"
    with open(path, "wb") as f:
        f.write(orjson.dumps(data))
    return str(path)

def save_seal(slug: str, seal: dict) -> str:
    Path(settings.SEALS_DIR).mkdir(parents=True, exist_ok=True)
    path = Path(settings.SEALS_DIR) / f"{slug}-seal.json"
    with open(path, "wb") as f:
        f.write(orjson.dumps(seal))
    return str(path)