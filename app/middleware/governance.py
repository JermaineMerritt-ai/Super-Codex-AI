"""
Governance Middleware for Super-Codex-AI

This middleware enforces governance rules, validates authority levels,
and ensures proper ceremonial compliance for all requests.
"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces governance rules and validates authority levels.
    
    Features:
    - Authority level validation for protected endpoints
    - Seal type verification for ceremonial operations
    - Council permission enforcement
    - Governance rule compliance checking
    """
    
    def __init__(
        self,
        app: ASGIApp,
        enforce_seals: bool = True,
        require_council_auth: bool = True,
        debug_mode: bool = False
    ):
        super().__init__(app)
        self.enforce_seals = enforce_seals
        self.require_council_auth = require_council_auth
        self.debug_mode = debug_mode
        
        # Define protected endpoints that require governance validation
        self.protected_endpoints = {
            "/api/governance/rules": {"min_authority": "Medium", "seal_required": True},
            "/api/governance/councils": {"min_authority": "High", "seal_required": True},
            "/api/ceremonial": {"min_authority": "High", "seal_required": True},
            "/api/admin": {"min_authority": "Maximum", "seal_required": True},
            "/api/restore": {"min_authority": "Maximum", "seal_required": True},
        }
        
        # Authority hierarchy (lowest to highest)
        self.authority_levels = {
            "Standard": 1,
            "Medium": 2,
            "High": 3,
            "Maximum": 4
        }
        
        # Valid seal types
        self.valid_seals = {
            "Custodian": "Standard",
            "Council": "Medium", 
            "Sacred": "High",
            "Eternal": "Maximum"
        }

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request through governance validation.
        """
        try:
            # Skip governance for health checks and static files
            if self._should_skip_governance(request):
                return await call_next(request)
            
            # Extract governance context from request
            governance_context = await self._extract_governance_context(request)
            
            # Validate governance requirements
            validation_result = await self._validate_governance(request, governance_context)
            
            if not validation_result["valid"]:
                return self._create_governance_error_response(
                    validation_result["error"],
                    validation_result.get("status_code", 403)
                )
            
            # Add governance context to request state
            request.state.governance = governance_context
            
            # Log governance validation
            if self.debug_mode:
                logger.info(f"Governance validated for {request.url.path}: {governance_context}")
            
            # Process the request
            response = await call_next(request)
            
            # Add governance headers to response
            self._add_governance_headers(response, governance_context)
            
            return response
            
        except Exception as e:
            logger.error(f"Governance middleware error: {str(e)}")
            return self._create_governance_error_response(
                "Internal governance validation error",
                500
            )

    def _should_skip_governance(self, request: Request) -> bool:
        """
        Determine if governance validation should be skipped for this request.
        """
        skip_paths = [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/static/",
            "/favicon.ico"
        ]
        
        path = request.url.path
        return any(path.startswith(skip_path) for skip_path in skip_paths)

    async def _extract_governance_context(self, request: Request) -> Dict[str, Any]:
        """
        Extract governance-related information from the request.
        """
        context = {
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
            "method": request.method,
            "authority_level": None,
            "seal_type": None,
            "actor": None,
            "realm": None,
            "council_auth": False
        }
        
        # Extract from headers
        headers = request.headers
        context["authority_level"] = headers.get("X-Authority-Level", "Standard")
        context["seal_type"] = headers.get("X-Seal-Type")
        context["actor"] = headers.get("X-Actor")
        context["realm"] = headers.get("X-Realm")
        
        # Check for council authorization
        auth_header = headers.get("authorization", "")
        if "council" in auth_header.lower():
            context["council_auth"] = True
        
        # Extract user context if available
        if hasattr(request.state, "user"):
            user = request.state.user
            context["user_id"] = getattr(user, "id", None)
            context["user_role"] = getattr(user, "role", None)
            if hasattr(user, "is_council") and user.is_council():
                context["council_auth"] = True
        
        return context

    async def _validate_governance(self, request: Request, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate governance requirements for the request.
        """
        path = request.url.path
        
        # Check if this endpoint requires governance validation
        protected_config = None
        for endpoint_pattern, config in self.protected_endpoints.items():
            if path.startswith(endpoint_pattern):
                protected_config = config
                break
        
        # If not protected, allow through
        if not protected_config:
            return {"valid": True}
        
        # Validate authority level
        required_authority = protected_config.get("min_authority", "Standard")
        user_authority = context.get("authority_level", "Standard")
        
        if not self._has_sufficient_authority(user_authority, required_authority):
            return {
                "valid": False,
                "error": f"Insufficient authority level. Required: {required_authority}, Provided: {user_authority}",
                "status_code": 403
            }
        
        # Validate seal requirement
        if self.enforce_seals and protected_config.get("seal_required", False):
            seal_type = context.get("seal_type")
            if not seal_type:
                return {
                    "valid": False,
                    "error": "Ceremonial seal required for this operation",
                    "status_code": 401
                }
            
            if seal_type not in self.valid_seals:
                return {
                    "valid": False,
                    "error": f"Invalid seal type: {seal_type}",
                    "status_code": 400
                }
            
            # Validate seal authority matches endpoint requirement
            seal_authority = self.valid_seals[seal_type]
            if not self._has_sufficient_authority(seal_authority, required_authority):
                return {
                    "valid": False,
                    "error": f"Seal authority insufficient. Required: {required_authority}, Seal provides: {seal_authority}",
                    "status_code": 403
                }
        
        # Validate council authorization for high-authority operations
        if self.require_council_auth and required_authority in ["High", "Maximum"]:
            if not context.get("council_auth", False):
                return {
                    "valid": False,
                    "error": "Council authorization required for this operation",
                    "status_code": 403
                }
        
        return {"valid": True}

    def _has_sufficient_authority(self, user_level: str, required_level: str) -> bool:
        """
        Check if user authority level meets the required level.
        """
        user_rank = self.authority_levels.get(user_level, 0)
        required_rank = self.authority_levels.get(required_level, 0)
        return user_rank >= required_rank

    def _create_governance_error_response(self, error_message: str, status_code: int) -> JSONResponse:
        """
        Create a standardized governance error response.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "error": "Governance Validation Failed",
                "message": error_message,
                "timestamp": datetime.now().isoformat(),
                "type": "governance_error"
            }
        )

    def _add_governance_headers(self, response: Response, context: Dict[str, Any]) -> None:
        """
        Add governance-related headers to the response.
        """
        response.headers["X-Governance-Validated"] = "true"
        response.headers["X-Governance-Timestamp"] = context["timestamp"]
        
        if context.get("authority_level"):
            response.headers["X-Authority-Level"] = context["authority_level"]
        
        if context.get("seal_type"):
            response.headers["X-Seal-Validated"] = context["seal_type"]