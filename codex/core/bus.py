from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on(self, evt: str, handler: Callable):
        self._handlers.setdefault(evt, []).append(handler)

    def emit(self, evt: str, payload: dict):
        for h in self._handlers.get(evt, []):
            h(payload)

bus = EventBus()