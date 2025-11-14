# engines/sigil.py
from core.identity import save_identity, save_seal
import hashlib, time

class SIGIL:
    def crown(self, name: str, roles: list[str]) -> dict:
        stamp = int(time.time())
        slug = hashlib.sha256(f"{name}-{stamp}".encode()).hexdigest()[:12]
        identity = {"name": name, "roles": roles, "slug": slug, "stamped_at": stamp}
        seal = {"slug": slug, "seal": f"SIGIL-{slug}", "status": "crowned"}
        save_identity(slug, identity)
        save_seal(slug, seal)
        return {"identity": identity, "seal": seal}