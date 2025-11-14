# engines/flame.py
from core.replay import archive

class FLAME:
    def dispatch(self, title: str, payload: dict) -> str:
        return archive(f"dispatch-{title}", payload)

    def closure(self, title: str, summary: str) -> str:
        return archive(f"closure-{title}", {"summary": summary, "status": "sealed"})
