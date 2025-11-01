"""
Registry for all Dominion protocol/agent services.
"""

from typing import Dict
from .base_protocol import DominionProtocolBase

class DominionProtocolRegistry:
    def __init__(self):
        self.protocols: Dict[str, DominionProtocolBase] = {}

    def register(self, protocol: DominionProtocolBase):
        self.protocols[protocol.name] = protocol

    def get_router(self):
        from fastapi import APIRouter
        router = APIRouter()
        for protocol in self.protocols.values():
            router.include_router(protocol.router)
        return router

registry = DominionProtocolRegistry()
