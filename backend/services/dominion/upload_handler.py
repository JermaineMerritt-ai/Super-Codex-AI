"""
Unified upload/onboarding handler for Dominion protocols/agents.
Automatically registers new modules in backend and dashboard registries.
"""

from .protocol_registry import registry
from .base_protocol import DominionProtocolBase

class DominionUploadHandler:
    def upload_protocol(self, protocol_class, name: str):
        protocol = protocol_class(name)
        protocol.register_routes()
        registry.register(protocol)
        # TODO: Add dashboard registration logic here
        return protocol

upload_handler = DominionUploadHandler()
