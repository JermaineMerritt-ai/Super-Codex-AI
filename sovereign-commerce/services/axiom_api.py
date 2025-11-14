#!/usr/bin/env python3
"""
AXIOM Engine API Routes for Sovereign Commerce Platform
Natural language invocation parsing and platform generation

Built with ceremonial dignity for intent recognition.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import core dependencies
from sovereign_main import get_db, get_current_user, User
from axiom_parser import axiom_parser

# Logging setup
logger = logging.getLogger(__name__)

# Create AXIOM API router
axiom_router = APIRouter(prefix="/api/axiom", tags=["AXIOM Engine"])

# Pydantic Models for AXIOM
class InvocationRequest(BaseModel):
    phrase: str

class ParsedIntentModel(BaseModel):
    appType: str
    audience: List[str]
    modules: List[str]
    style: List[str]

class InvocationResponse(BaseModel):
    original_phrase: str
    parsed_intent: ParsedIntentModel
    confidence: float
    recommendations: List[str]
    suggested_modules: List[str]
    platform_ready: bool

# ============================================================================
# AXIOM INTENT PARSER ENDPOINTS
# ============================================================================

@axiom_router.post("/parse", response_model=InvocationResponse)
async def parse_invocation_intent(
    request: InvocationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    🔮 AXIOM Intent Parser - Analyze natural language invocations
    
    Parse user invocations to extract structured intent for platform generation.
    """
    try:
        logger.info(f"AXIOM parsing invocation for {current_user.sigil}: '{request.phrase}'")
        
        # Parse the invocation using AXIOM engine
        analysis = axiom_parser.analyze_phrase(request.phrase)
        
        # Determine suggested modules based on intent
        suggested_modules = []
        intent = analysis['parsed_intent']
        
        if intent['appType'] == 'e-commerce':
            suggested_modules.extend(['product_catalog', 'checkout'])
        
        if 'diaspora funders' in intent['audience']:
            suggested_modules.append('funder_dashboard')
        
        if intent['style']:
            suggested_modules.append('contributor_recognition')
        
        # Remove duplicates and ensure valid modules
        suggested_modules = list(set(suggested_modules))
        
        # Check if platform is ready for this intent
        available_modules = ['product_catalog', 'checkout', 'funder_dashboard', 'contributor_recognition']
        platform_ready = all(module in available_modules for module in suggested_modules)
        
        response = InvocationResponse(
            original_phrase=request.phrase,
            parsed_intent=ParsedIntentModel(**analysis['parsed_intent']),
            confidence=analysis['confidence'],
            recommendations=analysis['recommendations'],
            suggested_modules=suggested_modules,
            platform_ready=platform_ready
        )
        
        logger.info(f"AXIOM analysis complete - Confidence: {analysis['confidence']:.2f}")
        return response
        
    except Exception as e:
        logger.error(f"AXIOM parsing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Intent parsing failed: {str(e)}")

@axiom_router.post("/generate")
async def generate_platform_from_intent(
    request: InvocationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🏗️ AXIOM Platform Generator - Generate platform from intent
    
    Automatically configure platform features based on parsed intent.
    """
    try:
        logger.info(f"AXIOM generating platform for {current_user.sigil}: '{request.phrase}'")
        
        # Parse the invocation
        analysis = axiom_parser.analyze_phrase(request.phrase)
        intent = analysis['parsed_intent']
        
        generation_plan = {
            "intent_analysis": intent,
            "confidence": analysis['confidence'],
            "enabled_modules": [],
            "generated_features": [],
            "ceremonial_elements": []
        }
        
        # Enable modules based on intent
        if 'product_catalog' in intent['modules']:
            generation_plan["enabled_modules"].append("product_catalog")
            generation_plan["generated_features"].append("Enhanced Product Catalog with Cultural Context")
        
        if 'checkout' in intent['modules']:
            generation_plan["enabled_modules"].append("checkout")
            generation_plan["generated_features"].append("Advanced Checkout System with Community Funds")
        
        if 'funder_dashboard' in intent['modules']:
            generation_plan["enabled_modules"].append("funder_dashboard")
            generation_plan["generated_features"].append("Diaspora Funder Dashboard with Cultural Insights")
        
        if 'contributor_recognition' in intent['modules']:
            generation_plan["enabled_modules"].append("contributor_recognition")
            generation_plan["generated_features"].append("Community Recognition System with Honors")
        
        # Add ceremonial elements based on style
        if 'mythic' in intent['style']:
            generation_plan["ceremonial_elements"].append("Sovereign interface themes")
            generation_plan["ceremonial_elements"].append("Mythic navigation patterns")
        
        if 'ceremonial' in intent['style']:
            generation_plan["ceremonial_elements"].append("Scroll-based documentation")
            generation_plan["ceremonial_elements"].append("Ceremonial user flows")
        
        # Special handling for diaspora funders
        if 'diaspora funders' in intent['audience']:
            generation_plan["ceremonial_elements"].append("Cultural context integration")
            generation_plan["ceremonial_elements"].append("Community-focused features")
        
        logger.info(f"AXIOM platform generation plan created with {len(generation_plan['enabled_modules'])} modules")
        
        return JSONResponse(content={
            "status": "generated",
            "message": "Platform configuration generated from intent",
            "generation_plan": generation_plan,
            "ready_for_deployment": len(generation_plan["enabled_modules"]) > 0,
            "generated_by": current_user.sigil,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"AXIOM platform generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Platform generation failed: {str(e)}")

@axiom_router.get("/test")
async def test_axiom_parser():
    """
    🧪 AXIOM Test Suite - Test the intent parser with sample phrases
    """
    try:
        test_phrases = [
            "sovereign commerce scroll for diaspora funders",
            "create catalog and checkout system",
            "dashboard with recognition features",
            "ceremonial sovereign platform",
            "simple product catalog",
            "diaspora funder analytics dashboard"
        ]
        
        test_results = []
        for phrase in test_phrases:
            analysis = axiom_parser.analyze_phrase(phrase)
            test_results.append({
                "phrase": phrase,
                "intent": analysis['parsed_intent'],
                "confidence": analysis['confidence'],
                "recommendations": analysis['recommendations']
            })
        
        return JSONResponse(content={
            "status": "test_complete",
            "message": "AXIOM parser test suite completed",
            "test_results": test_results,
            "total_tests": len(test_phrases),
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"AXIOM test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

def get_axiom_router() -> APIRouter:
    """Get the AXIOM API router"""
    return axiom_router