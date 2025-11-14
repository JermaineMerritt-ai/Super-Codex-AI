# engines/lantern.py
class LANTERN:
    def onboarding_steps(self, role: str) -> list[str]:
        return [
            "Accept sovereign charter",
            "Link identity and seal",
            f"Initialize scroll logic for role: {role}",
            "Complete audit and replay handshake",
            "Receive dispatch permissions"
        ]