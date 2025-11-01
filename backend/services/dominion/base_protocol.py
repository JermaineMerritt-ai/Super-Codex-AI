"""
Base class for Dominion protocol/agent services.
"""

from fastapi import APIRouter

class DominionProtocolBase:
    def __init__(self, name: str):
        self.name = name
        self.router = APIRouter(prefix=f"/dominion/{name}")

    def register_routes(self):
        # To be implemented by subclasses
        pass
