#!/usr/bin/env python3
"""
Enhanced API Routes for Sovereign Commerce Platform
Integrating diaspora-focused modules: Product Catalog, Checkout, Dashboard, and Recognition

Built with ceremonial dignity for the complete diaspora funder experience.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# Import our enhanced services
from sovereign_main import get_db, get_current_user, User
from axiom_parser import axiom_parser, ParsedIntent

# Late imports to avoid circular dependencies - these will be imported in the functions where needed
# from product_catalog import DiasporaProductCatalog, get_diaspora_catalog_service
# from checkout_system import DiasporaCheckoutService, get_diaspora_checkout_service
# from funder_dashboard import DiasporaFunderDashboard, get_diaspora_dashboard_service
# from contributor_recognition import ContributorRecognitionService, get_recognition_service

# Logging setup
logger = logging.getLogger(__name__)

# Create API router
enhanced_router = APIRouter(prefix="/api/enhanced", tags=["Enhanced Diaspora Features"])

# Pydantic Models for Enhanced Features

# Product Catalog Models
class CategoryCreate(BaseModel):
    name: str
    description: str
    cultural_significance: str

class CulturalCollectionCreate(BaseModel):
    name: str
    description: str
    diaspora_region: str
    metadata: Optional[Dict] = None

class ProductAttributeCreate(BaseModel):
    attribute_type: str
    attribute_name: str
    attribute_value: str

class ProductReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review_text: str
    cultural_context: Optional[str] = None

class ProductCatalogFilter(BaseModel):
    category_filter: Optional[str] = None
    diaspora_region: Optional[str] = None
    cultural_significance: Optional[str] = None

# Checkout System Models
class PaymentMethodCreate(BaseModel):
    name: str
    description: str
    payment_type: str
    cultural_context: str
    requires_verification: bool = False

class CommunityFundCreate(BaseModel):
    fund_name: str
    description: str
    target_region: str
    current_goal: Decimal
    fund_purpose: str

class CheckoutSessionInit(BaseModel):
    cart_items: List[Dict]
    cultural_preferences: Optional[Dict] = None

class CheckoutSessionUpdate(BaseModel):
    shipping_address: Optional[Dict] = None
    payment_method_id: Optional[str] = None
    community_fund_contribution: Optional[Decimal] = None

class CeremonialCheckout(BaseModel):
    ceremony_preferences: Optional[Dict] = None
    selected_fund_id: Optional[str] = None

# Dashboard Models
class FunderPreferencesUpdate(BaseModel):
    cultural_regions: Optional[List[str]] = None
    preferred_languages: Optional[List[str]] = None
    community_interests: Optional[List[str]] = None
    notification_preferences: Optional[Dict] = None
    dashboard_layout: Optional[Dict] = None
    privacy_settings: Optional[Dict] = None

class ActivityRecord(BaseModel):
    activity_type: str
    activity_data: Dict
    cultural_significance: Optional[str] = None

# AXIOM Parser Models
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
    community_impact: Optional[str] = None

# Recognition System Models
class ContributorProfileCreate(BaseModel):
    display_name: str
    bio_statement: str
    cultural_heritage: Dict
    expertise_areas: List[str]
    contribution_categories: Optional[List[str]] = None

class ContributionRecord(BaseModel):
    contribution_category: str
    contribution_type: str
    contribution_title: str
    contribution_description: str
    cultural_impact: str
    beneficiary_community: str
    contribution_evidence: Optional[Dict] = None

class HonorCreate(BaseModel):
    honor_title: str
    honor_description: str
    cultural_significance: str
    required_categories: List[str]
    minimum_honor_points: int
    minimum_recognition_level: str
    honor_ceremony: Dict

class HonorAward(BaseModel):
    ceremony_details: Dict
    community_witnesses: Optional[List[str]] = None
    cultural_blessing: Optional[str] = None

class EndorsementCreate(BaseModel):
    endorsement_category: str
    endorsement_text: str
    cultural_context: str
    strength_rating: int = Field(..., ge=1, le=10)

# ========== ENHANCED PRODUCT CATALOG ROUTES ==========

@enhanced_router.post("/catalog/categories")
async def create_product_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product category with cultural significance"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.create_category(
        name=category_data.name,
        description=category_data.description,
        cultural_significance=category_data.cultural_significance,
        creator_role=current_user.role
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/catalog/collections")
async def create_cultural_collection(
    collection_data: CulturalCollectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a cultural collection for diaspora regions"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.create_cultural_collection(
        name=collection_data.name,
        description=collection_data.description,
        diaspora_region=collection_data.diaspora_region,
        curator_id=current_user.id,
        metadata_json=collection_data.metadata
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/catalog/products/{product_id}/attributes")
async def add_product_attribute(
    product_id: str,
    attribute_data: ProductAttributeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add cultural or ceremonial attributes to products"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.add_product_attribute(
        product_id=product_id,
        attribute_type=attribute_data.attribute_type,
        attribute_name=attribute_data.attribute_name,
        attribute_value=attribute_data.attribute_value
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/catalog/products/{product_id}/reviews")
async def create_product_review(
    product_id: str,
    review_data: ProductReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a product review with cultural context"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.create_product_review(
        product_id=product_id,
        user_id=current_user.id,
        rating=review_data.rating,
        review_text=review_data.review_text,
        cultural_context=review_data.cultural_context
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.get("/catalog/enhanced")
async def get_enhanced_catalog(
    category_filter: Optional[str] = None,
    diaspora_region: Optional[str] = None,
    cultural_significance: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get enhanced product catalog with cultural context"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.get_enhanced_product_catalog(
        category_filter=category_filter,
        diaspora_region=diaspora_region,
        cultural_significance=cultural_significance
    )
    
    return JSONResponse(content=result)

@enhanced_router.get("/catalog/products/{product_id}/cultural")
async def get_product_cultural_context(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed product information with full cultural context"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.get_product_with_cultural_context(product_id)
    
    return JSONResponse(content=result)

@enhanced_router.get("/catalog/collections/by-region")
async def get_collections_by_region(
    diaspora_region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get cultural collections for specific diaspora regions"""
    from product_catalog import get_diaspora_catalog_service
    catalog_service = get_diaspora_catalog_service(db)
    
    result = catalog_service.get_collections_by_region(diaspora_region)
    
    return JSONResponse(content=result)

# ========== ENHANCED CHECKOUT SYSTEM ROUTES ==========

@enhanced_router.post("/checkout/payment-methods")
async def create_payment_method(
    payment_data: PaymentMethodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new payment method with cultural context"""
    if current_user.role not in ["flamekeeper", "custodian"]:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.create_payment_method(
        name=payment_data.name,
        description=payment_data.description,
        payment_type=payment_data.payment_type,
        cultural_context=payment_data.cultural_context,
        requires_verification=payment_data.requires_verification
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/checkout/community-funds")
async def create_community_fund(
    fund_data: CommunityFundCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a community fund for diaspora support"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.create_community_fund(
        fund_name=fund_data.fund_name,
        description=fund_data.description,
        target_region=fund_data.target_region,
        current_goal=fund_data.current_goal,
        fund_purpose=fund_data.fund_purpose,
        manager_id=current_user.id
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/checkout/sessions")
async def initialize_checkout_session(
    session_data: CheckoutSessionInit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initialize a checkout session with cultural preferences"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.initialize_checkout_session(
        user_id=current_user.id,
        cart_items=session_data.cart_items,
        cultural_preferences=session_data.cultural_preferences
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.put("/checkout/sessions/{session_id}")
async def update_checkout_session(
    session_id: str,
    update_data: CheckoutSessionUpdate,
    session_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update checkout session with shipping and payment details"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.update_checkout_session(
        session_id=session_id,
        session_token=session_token,
        shipping_address=update_data.shipping_address,
        payment_method_id=update_data.payment_method_id,
        community_fund_contribution=update_data.community_fund_contribution
    )
    
    return JSONResponse(content=result)

@enhanced_router.post("/checkout/sessions/{session_id}/complete")
async def complete_ceremonial_checkout(
    session_id: str,
    checkout_data: CeremonialCheckout,
    session_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete the ceremonial checkout process"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.complete_ceremonial_checkout(
        session_id=session_id,
        session_token=session_token,
        ceremony_preferences=checkout_data.ceremony_preferences,
        selected_fund_id=checkout_data.selected_fund_id
    )
    
    return JSONResponse(content=result)

@enhanced_router.get("/checkout/payment-methods")
async def get_payment_methods(
    payment_type_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get available payment methods with cultural context"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.get_available_payment_methods(payment_type_filter)
    
    return JSONResponse(content=result)

@enhanced_router.get("/checkout/community-funds")
async def get_community_funds(
    target_region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get community funds available for contributions"""
    from checkout_system import get_diaspora_checkout_service
    checkout_service = get_diaspora_checkout_service(db)
    
    result = checkout_service.get_community_funds(target_region)
    
    return JSONResponse(content=result)

# ========== DIASPORA FUNDER DASHBOARD ROUTES ==========

@enhanced_router.get("/dashboard/overview")
async def get_funder_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive funder overview"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.get_funder_overview(current_user.id)
    
    return JSONResponse(content=result)

@enhanced_router.get("/dashboard/cultural-insights")
async def get_cultural_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized cultural insights for the funder"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.get_cultural_insights(current_user.id)
    
    return JSONResponse(content=result)

@enhanced_router.get("/dashboard/community")
async def get_community_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get community-focused dashboard with connections and collaborations"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.get_community_dashboard(current_user.id)
    
    return JSONResponse(content=result)

@enhanced_router.get("/dashboard/recommendations")
async def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations based on cultural profile and activity"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.get_personalized_recommendations(current_user.id)
    
    return JSONResponse(content=result)

@enhanced_router.put("/dashboard/preferences")
async def update_funder_preferences(
    preferences_data: FunderPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update funder preferences and dashboard settings"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.update_funder_preferences(
        user_id=current_user.id,
        preferences_data=preferences_data.dict(exclude_unset=True)
    )
    
    return JSONResponse(content=result)

@enhanced_router.post("/dashboard/activity")
async def record_funder_activity(
    activity_data: ActivityRecord,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record funder activity for dashboard tracking"""
    from funder_dashboard import get_diaspora_dashboard_service
    dashboard_service = get_diaspora_dashboard_service(db)
    
    result = dashboard_service.record_funder_activity(
        user_id=current_user.id,
        activity_type=activity_data.activity_type,
        activity_data=activity_data.activity_data,
        cultural_significance=activity_data.cultural_significance,
        community_impact=activity_data.community_impact
    )
    
    return JSONResponse(content=result, status_code=201)

# ========== CONTRIBUTOR RECOGNITION ROUTES ==========

@enhanced_router.post("/recognition/profiles")
async def create_contributor_profile(
    profile_data: ContributorProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a contributor profile"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.create_contributor_profile(
        user_id=current_user.id,
        display_name=profile_data.display_name,
        bio_statement=profile_data.bio_statement,
        cultural_heritage=profile_data.cultural_heritage,
        expertise_areas=profile_data.expertise_areas,
        contribution_categories=profile_data.contribution_categories
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/recognition/contributions")
async def record_contribution(
    contribution_data: ContributionRecord,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a new contribution"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    # Get contributor profile ID for current user
    from contributor_recognition import ContributorProfile
    contributor = db.query(ContributorProfile).filter(
        ContributorProfile.user_id == current_user.id
    ).first()
    
    if not contributor:
        raise HTTPException(status_code=404, detail="Contributor profile not found. Please create one first.")
    
    result = recognition_service.record_contribution(
        contributor_id=contributor.id,
        contribution_category=contribution_data.contribution_category,
        contribution_type=contribution_data.contribution_type,
        contribution_title=contribution_data.contribution_title,
        contribution_description=contribution_data.contribution_description,
        cultural_impact=contribution_data.cultural_impact,
        beneficiary_community=contribution_data.beneficiary_community,
        contribution_evidence=contribution_data.contribution_evidence
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/recognition/contributions/{record_id}/verify")
async def verify_contribution(
    record_id: str,
    verification_notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify a contribution record (flamekeeper/custodian only)"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.verify_contribution(
        record_id=record_id,
        verifier_id=current_user.id,
        verification_notes=verification_notes
    )
    
    return JSONResponse(content=result)

@enhanced_router.post("/recognition/honors")
async def create_community_honor(
    honor_data: HonorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new community honor"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.create_community_honor(
        honor_title=honor_data.honor_title,
        honor_description=honor_data.honor_description,
        cultural_significance=honor_data.cultural_significance,
        required_categories=honor_data.required_categories,
        minimum_honor_points=honor_data.minimum_honor_points,
        minimum_recognition_level=honor_data.minimum_recognition_level,
        honor_ceremony=honor_data.honor_ceremony,
        creator_role=current_user.role
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.post("/recognition/honors/{honor_id}/award/{contributor_id}")
async def award_honor(
    honor_id: str,
    contributor_id: str,
    award_data: HonorAward,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award a community honor to a contributor"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.award_honor(
        honor_id=honor_id,
        contributor_id=contributor_id,
        awarded_by=current_user.id,
        ceremony_details=award_data.ceremony_details,
        community_witnesses=award_data.community_witnesses,
        cultural_blessing=award_data.cultural_blessing
    )
    
    return JSONResponse(content=result)

@enhanced_router.post("/recognition/contributors/{contributor_id}/endorse")
async def create_endorsement(
    contributor_id: str,
    endorsement_data: EndorsementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an endorsement between contributors"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    # Get endorser's contributor profile ID
    from contributor_recognition import ContributorProfile
    endorser = db.query(ContributorProfile).filter(
        ContributorProfile.user_id == current_user.id
    ).first()
    
    if not endorser:
        raise HTTPException(status_code=404, detail="Your contributor profile not found. Please create one first.")
    
    result = recognition_service.create_endorsement(
        contributor_id=contributor_id,
        endorser_id=endorser.id,
        endorsement_category=endorsement_data.endorsement_category,
        endorsement_text=endorsement_data.endorsement_text,
        cultural_context=endorsement_data.cultural_context,
        strength_rating=endorsement_data.strength_rating
    )
    
    return JSONResponse(content=result, status_code=201)

@enhanced_router.get("/recognition/contributors/{contributor_id}")
async def get_contributor_profile(
    contributor_id: str,
    db: Session = Depends(get_db)
):
    """Get comprehensive contributor recognition profile"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.get_contributor_recognition_profile(contributor_id)
    
    return JSONResponse(content=result)

@enhanced_router.get("/recognition/leaderboard")
async def get_community_leaderboard(
    category_filter: Optional[str] = None,
    region_filter: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get community leaderboard of top contributors"""
    from contributor_recognition import get_recognition_service
    recognition_service = get_recognition_service(db)
    
    result = recognition_service.get_community_leaderboard(
        category_filter=category_filter,
        region_filter=region_filter,
        limit=min(limit, 100)  # Cap at 100 for performance
    )
    
    return JSONResponse(content=result)

# ========== SYSTEM STATUS AND HEALTH ROUTES ==========

@enhanced_router.get("/status")
async def get_enhanced_system_status(db: Session = Depends(get_db)):
    """Get status of all enhanced systems"""
    try:
        # Import all service functions locally
        from product_catalog import get_diaspora_catalog_service
        from checkout_system import get_diaspora_checkout_service
        from funder_dashboard import get_diaspora_dashboard_service
        from contributor_recognition import get_recognition_service
        
        # Test each service
        catalog_service = get_diaspora_catalog_service(db)
        checkout_service = get_diaspora_checkout_service(db)
        dashboard_service = get_diaspora_dashboard_service(db)
        recognition_service = get_recognition_service(db)
        
        # Get basic counts for health check
        from product_catalog import ProductCategory, CulturalCollection
        from checkout_system import PaymentMethod, CommunityFund
        from contributor_recognition import ContributorProfile, CommunityHonor
        
        category_count = db.query(ProductCategory).count()
        collection_count = db.query(CulturalCollection).count()
        payment_method_count = db.query(PaymentMethod).count()
        fund_count = db.query(CommunityFund).count()
        contributor_count = db.query(ContributorProfile).count()
        honor_count = db.query(CommunityHonor).count()
        
        return JSONResponse(content={
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "product_catalog": {
                    "status": "healthy",
                    "categories": category_count,
                    "collections": collection_count
                },
                "checkout_system": {
                    "status": "healthy",
                    "payment_methods": payment_method_count,
                    "community_funds": fund_count
                },
                "dashboard": {
                    "status": "healthy"
                },
                "recognition": {
                    "status": "healthy",
                    "contributors": contributor_count,
                    "honors": honor_count
                }
            },
            "message": "Enhanced diaspora systems operational with cultural honors"
        })
        
    except Exception as e:
        logger.error(f"Enhanced system status check failed: {e}")
        return JSONResponse(
            content={
                "status": "degraded",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            },
            status_code=503
        )

# Initialize all enhanced features (for testing and seeding)
@enhanced_router.post("/initialize")
async def initialize_enhanced_features(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initialize all enhanced features with sample data (custodian only)"""
    if current_user.role != "custodian":
        raise HTTPException(status_code=403, detail="Only custodians can initialize enhanced features")
    
    try:
        # Import seeding functions
        from product_catalog import seed_sample_categories, seed_sample_collections
        from checkout_system import seed_payment_methods, seed_community_funds
        from contributor_recognition import seed_community_honors
        
        # Initialize sample data
        seed_sample_categories(db)
        seed_sample_collections(db, current_user.id)
        seed_payment_methods(db)
        seed_community_funds(db, current_user.id)
        seed_community_honors(db)
        
        logger.info(f"Enhanced features initialized by {current_user.sigil}")
        
        return JSONResponse(content={
            "status": "initialized",
            "message": "Enhanced diaspora features initialized with sample data",
            "initialized_by": current_user.sigil,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Enhanced features initialization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

# ============================================================================
# AXIOM INTENT PARSER ENDPOINTS
# ============================================================================

@enhanced_router.post("/axiom/parse", response_model=InvocationResponse, tags=["AXIOM Engine"])
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

@enhanced_router.post("/axiom/generate", tags=["AXIOM Engine"])
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

@enhanced_router.get("/axiom/test", tags=["AXIOM Engine"])
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

def get_enhanced_router() -> APIRouter:
    """Get the enhanced API router"""
    return enhanced_router