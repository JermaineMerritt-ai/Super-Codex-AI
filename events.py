from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    stream_id: str
    name: str
    payload: dict
    at: datetime

# Examples:
# ArtifactCreated, ArtifactSealed, CeremonyScheduled, CeremonyStarted, OathRecited, CeremonySealed