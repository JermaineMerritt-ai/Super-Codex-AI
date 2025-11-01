from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Capsule logic

import os

class CodexAutomationCapsule:
    LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/capsule_events.log")

    def __init__(self, custodian_id, sector, epoch):
        self.custodian_id = custodian_id
        self.sector = sector
        self.epoch = epoch
        self.replay_log = []
        self.invocation_keys = {
            "finance": "Invoke Ledger Flame",
            "education": "Invoke Scroll of Insight",
            "diaspora": "Invoke Ancestral Dispatch",
            "governance": "Invoke Seal of Accord"
        }

    def activate_capsule(self):
        log_entry = self.log_replay()
        modules = self.trigger_modules()
        artifacts = self.dispatch_artifacts()
        oathstone = self.bind_oathstone()
        self.log_event({
            "event": "activation",
            "custodian": self.custodian_id,
            "sector": self.sector,
            "epoch": self.epoch,
            "timestamp": self.get_timestamp()
        })
        return {
            "log": log_entry,
            "modules": modules,
            "artifacts": artifacts,
            "oathstone": oathstone,
            "message": "Codex Capsule Activated: Sovereign Replay Initiated"
        }

    def log_replay(self):
        entry = {
            "custodian": self.custodian_id,
            "sector": self.sector,
            "epoch": self.epoch,
            "timestamp": self.get_timestamp()
        }
        self.replay_log.append(entry)
        self.log_event({"event": "replay", **entry})
        return entry

    def trigger_modules(self):
        modules = [
            "Engine Invocation Scroll",
            "Resolution Engine",
            "Truth Capsule",
            "Replay Shell"
        ]
        return modules

    def dispatch_artifacts(self):
        artifacts = [
            "Capsule Series",
            "Replay Deck",
            "Contributor Recognition"
        ]
        return artifacts

    def bind_oathstone(self):
        return "Oathstone Bound: Eternal Custodian Vow Inscribed"

    def invoke_sector_key(self, domain):
        key = self.invocation_keys.get(domain.lower())
        if key:
            self.log_event({
                "event": "invocation",
                "domain": domain,
                "key": key,
                "timestamp": self.get_timestamp()
            })
            return f"Sectoral Invocation Triggered: {key}"
        else:
            return "No invocation key found for this domain."

    def get_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def log_event(self, event):
        os.makedirs(os.path.dirname(self.LOG_PATH), exist_ok=True)
        with open(self.LOG_PATH, "a") as f:
            f.write(f"{event}\n")

# FastAPI router
router = APIRouter()

class CapsuleRequest(BaseModel):
    custodian_id: str
    sector: str
    epoch: str
    domain: Optional[str] = None

@router.post("/api/capsule/activate")
def activate_capsule(req: CapsuleRequest):
    capsule = CodexAutomationCapsule(req.custodian_id, req.sector, req.epoch)
    result = capsule.activate_capsule()
    if req.domain:
        result["invocation"] = capsule.invoke_sector_key(req.domain)
    return result
