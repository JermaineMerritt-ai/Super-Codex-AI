# great_year_rite.py
# Millennial proclamation script for Codex Dominion
from pathlib import Path
import json, datetime, uuid

BASE = Path(__file__).resolve().parent
STORAGE = BASE / "storage"
GREATYEAR = STORAGE / "greatyear"
GREATYEAR.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def epoch_key(dt):
    # Define epochs by millennia
    return f"{(dt.year // 1000) * 1000}-{((dt.year // 1000) * 1000) + 999}"

def great_year_proclamation():
    dt = datetime.datetime.utcnow()
    epoch = epoch_key(dt)
    proclamation_id = f"GYR-{epoch}-{str(uuid.uuid4())[:8]}"

    proclamation = {
        "schema": "greatyear.v1",
        "proclamation_id": proclamation_id,
        "timestamp": now_iso(),
        "epoch": epoch,
        "summary": f"Great Year Rite: Crown of Epoch {epoch}, flame sealed for millennia.",
        "audit": {"status": "Sealed", "authority": "Custodian Crown"}
    }

    (GREATYEAR / f"{proclamation_id}.json").write_text(json.dumps(proclamation, indent=2), encoding="utf-8")
    print(f"[GREAT YEAR] {proclamation['summary']}")

if __name__ == "__main__":
    great_year_proclamation()