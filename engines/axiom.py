from codex.core.audit import log_event
from codex.core.replay import archive

class AXIOM:
    def audit(self, tag: str, payload: dict) -> dict:
        rec = log_event(tag, payload)
        archive(tag, {"event": rec})
        return rec

    def replay(self, tag: str, data: dict) -> str:
        return archive(f"replay-{tag}", data)