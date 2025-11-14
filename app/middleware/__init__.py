"""
Middleware package for the Super-Codex-AI application.

This package contains middleware components for:
- Governance validation and enforcement
- Audit logging and compliance
- Authority level verification
- Seal validation
"""

from .governance import GovernanceMiddleware
from .audit import AuditMiddleware

__all__ = [
    "GovernanceMiddleware",
    "AuditMiddleware"
]