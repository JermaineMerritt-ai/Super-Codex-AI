#!/usr/bin/env python3
"""
Sovereign Commerce Platform
A ceremonial marketplace for Diaspora Funders

Built with mythic dignity and sovereign recognition.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import jwt
from passlib.hash import bcrypt
from sqlalchemy import create_engine, Column, String, DateTime, DECIMAL, Integer, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import secrets
import httpx
import json
import uuid

# Logging setup - must be early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SOVEREIGN-COMMERCE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Sovereign Commerce Platform
app = FastAPI(
    title="Sovereign Commerce Platform",
    description="A ceremonial marketplace for Diaspora Funders",
    version="1.0.0",
    docs_url="/sacred/docs",
    redoc_url="/sacred/redoc"
)

# CORS configuration for diaspora accessibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
current_dir = Path(__file__).parent.parent  # Go up from services/ to sovereign-commerce/
db_dir = current_dir / 'db'
db_dir.mkdir(exist_ok=True)  # Ensure db directory exists
DATABASE_URL = f"sqlite:///{db_dir / 'sovereign_commerce.db'}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Authentication
security = HTTPBearer()

# AXIOM-FLAME Configuration
AXIOM_FLAME_BASE = "http://127.0.0.1:5000"  # AXIOM-FLAME API endpoint
AXIOM_FLAME_TIMEOUT = 30

# Templates and Static Files
current_dir = Path(__file__).parent.parent  # Go up from services/ to sovereign-commerce/
template_dir = current_dir / "ui" / "templates"
static_dir = current_dir / "ui" / "static"

logger.info(f"🔍 Looking for template directory at: {template_dir}")
logger.info(f"🔍 Looking for static directory at: {static_dir}")

# Verify directories exist
if not template_dir.exists():
    logger.error(f"Template directory not found: {template_dir}")
    raise FileNotFoundError(f"Template directory not found: {template_dir}")

if not static_dir.exists():
    logger.error(f"Static directory not found: {static_dir}")
    raise FileNotFoundError(f"Static directory not found: {static_dir}")

logger.info("✅ Template and static directories found")

templates = Jinja2Templates(directory=str(template_dir))
# Mount static files for sovereign styling
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # funder, flamekeeper, custodian
    sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    currency = Column(String, default="USD")
    category = Column(String)
    stock = Column(Integer, default=0)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    product_metadata = Column(Text)  # JSON string for ceremonial details

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    total_amount = Column(DECIMAL(10, 2))
    currency = Column(String, default="USD")
    status = Column(String)  # pending, confirmed, fulfilled, honored
    created_at = Column(DateTime, default=datetime.utcnow)
    fulfilled_at = Column(DateTime)
    ceremonial_seal = Column(String)  # Unique seal for each order

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True)
    order_id = Column(String)
    product_id = Column(String)
    quantity = Column(Integer)
    unit_price = Column(DECIMAL(10, 2))
    total_price = Column(DECIMAL(10, 2))

class Build(Base):
    __tablename__ = "builds"
    
    id = Column(String, primary_key=True)
    artifact_id = Column(String, unique=True)
    title = Column(String)
    version = Column(String)
    type = Column(String)
    engines = Column(Text)  # JSON array
    audience = Column(Text)  # JSON array
    sigil = Column(String, unique=True)
    signed_by = Column(String)
    authority = Column(String)
    status = Column(String, default="registered")
    dispatch_id = Column(String, unique=True)  # AXIOM-FLAME dispatch ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    build_metadata = Column(Text)  # Full build specification as JSON

class BuildDispatch(Base):
    __tablename__ = "build_dispatches"
    
    id = Column(String, primary_key=True)
    build_id = Column(String)
    dispatch_id = Column(String, unique=True)
    actor = Column(String)
    realm = Column(String)
    capsule = Column(String)
    intent = Column(String)
    status = Column(String)
    response_data = Column(Text)  # JSON response from AXIOM-FLAME
    created_at = Column(DateTime, default=datetime.utcnow)

class BuildReplay(Base):
    __tablename__ = "build_replays"
    
    id = Column(String, primary_key=True)
    build_id = Column(String)
    original_dispatch_id = Column(String)
    replay_id = Column(String, unique=True)
    replay_data = Column(Text)  # JSON replay data
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Import enhanced modules to register their tables
try:
    from product_catalog import ProductCategory, ProductAttribute, ProductReview, CulturalCollection, ProductCollection
    from checkout_system import PaymentMethod, CheckoutSession, CommunityFund, FundContribution, OrderCeremony
    from funder_dashboard import FunderActivity, FunderMilestone, CommunityConnection, FunderRecommendation, FunderPreference
    from contributor_recognition import ContributorProfile, ContributionRecord, CommunityHonor, HonorAwarded, ContributorEndorsement, CommunityRecognitionEvent
    logger.info("✅ Enhanced modules imported successfully")
except Exception as e:
    logger.error(f"❌ Error importing enhanced modules: {e}")

# Create tables (including enhanced tables)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ All database tables created successfully")
except Exception as e:
    logger.error(f"❌ Database table creation failed: {e}")

# Pydantic Models
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "funder"

class UserLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str
    image_url: Optional[str] = None
    metadata: Optional[Dict] = None

class CartItem(BaseModel):
    product_id: str
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    payment_method: str = "ceremonial_tribute"

class BuildRegistration(BaseModel):
    artifact_id: str
    title: str
    version: str
    type: str
    engines: List[str]
    audience: List[str]
    files: Dict[str, str]
    signing: Dict[str, str]
    platform: Optional[Dict] = None
    features: Optional[Dict] = None
    endpoints: Optional[Dict] = None
    governance: Optional[Dict] = None

class GlobalDispatchRequest(BaseModel):
    build_id: str
    actor: str = "Custodian"
    realm: str = "Sovereign-Commerce"
    capsule: str = "Build-Deployment"
    intent: str = "Global.Dispatch"
    target_environments: Optional[List[str]] = None

class BuildReplayRequest(BaseModel):
    build_id: str
    original_dispatch_id: str
    replay_context: Optional[Dict] = None

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

def get_password_hash(password):
    return bcrypt.hash(password)

def generate_sigil():
    """Generate a unique ceremonial sigil for users"""
    return f"SIGIL-{secrets.token_hex(4).upper()}"

def generate_ceremonial_seal():
    """Generate a unique ceremonial seal for orders"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"SEAL-{timestamp}-{secrets.token_hex(4).upper()}"

def generate_build_sigil():
    """Generate a unique SIGIL for builds"""
    return f"SIGIL-BUILD-{secrets.token_hex(4).upper()}"

def generate_dispatch_id():
    """Generate AXIOM-FLAME compatible dispatch ID"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    return f"AXF-{timestamp}-{str(uuid.uuid4())[:8]}"

async def call_axiom_flame(endpoint: str, method: str = "POST", data: dict = None):
    """Call AXIOM-FLAME API with proper error handling"""
    url = f"{AXIOM_FLAME_BASE}/api/{endpoint}"
    
    try:
        async with httpx.AsyncClient(timeout=AXIOM_FLAME_TIMEOUT) as client:
            if method == "GET":
                response = await client.get(url)
            else:
                response = await client.post(url, json=data)
            
            if response.status_code >= 400:
                logger.error(f"AXIOM-FLAME error {response.status_code}: {response.text}")
                return None, f"AXIOM-FLAME error: {response.status_code}"
            
            return response.json(), None
            
    except httpx.ConnectError as e:
        logger.error(f"AXIOM-FLAME connection error: {e}")
        return None, "AXIOM-FLAME service unavailable"
    except Exception as e:
        logger.error(f"AXIOM-FLAME call error: {e}")
        return None, f"AXIOM-FLAME error: {str(e)}"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Import enhanced API router and AXIOM engine
try:
    from enhanced_api import get_enhanced_router
    enhanced_router = get_enhanced_router()
    app.include_router(enhanced_router)
    logger.info("✅ Enhanced API routes included")
except Exception as e:
    logger.error(f"❌ Error including enhanced API routes: {e}")

# Import AXIOM API router (separate to avoid circular imports)
try:
    from axiom_api import get_axiom_router
    axiom_router = get_axiom_router()
    app.include_router(axiom_router)
    logger.info("✅ AXIOM Engine API routes included")
except Exception as e:
    logger.error(f"❌ Error including AXIOM API routes: {e}")

# Import Orchestrator API router
try:
    from orchestrator_api import orchestrator_router
    app.include_router(orchestrator_router)
    logger.info("✅ AXIOM-FLAME Orchestrator API routes included")
    
    # Include Codex Sovereign Suite components
    try:
        from sovereign_suite import get_sovereign_suite_router
        suite_router = get_sovereign_suite_router()
        app.include_router(suite_router)
        logger.info("🌟 Codex Sovereign Suite routes included")
        
        from portfolio_capsule import get_portfolio_capsule_router  
        portfolio_router = get_portfolio_capsule_router()
        app.include_router(portfolio_router)
        logger.info("🎨 Portfolio Capsule routes included")
        
        from funder_dashboard import get_enhanced_dashboard_router
        dashboard_router = get_enhanced_dashboard_router()
        app.include_router(dashboard_router)
        logger.info("👑 Enhanced Funder Dashboard routes included")
        
        from mythic_design_system import get_mythic_design_system, generate_mythic_css
        mythic_system = get_mythic_design_system()
        logger.info("✨ Mythic Design System initialized")
        
    except ImportError as e:
        logger.warning(f"⚠️ Some Codex Suite components not available: {e}")
        
    logger.info("🔥 CODEX SOVEREIGN SUITE FULLY INTEGRATED")
except Exception as e:
    logger.error(f"❌ Error including Orchestrator API routes: {e}")

# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main commerce portal"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request, db: Session = Depends(get_db)):
    """Product catalog for diaspora funders"""
    products = db.query(Product).filter(Product.is_active == True).all()
    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "products": products
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    """Funder dashboard"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user
    })

# API Routes
@app.post("/api/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new funder"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_id = f"USER-{secrets.token_hex(8).upper()}"
    hashed_password = get_password_hash(user_data.password)
    sigil = generate_sigil()
    
    new_user = User(
        id=user_id,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        sigil=sigil
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New funder registered: {user_data.email} with sigil {sigil}")
    
    return {
        "message": "Funder registered with ceremonial honors",
        "user_id": user_id,
        "sigil": sigil
    }

@app.post("/api/login")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate funder"""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    logger.info(f"Funder authenticated: {user.email} ({user.sigil})")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "sigil": user.sigil
        }
    }

@app.get("/api/products")
async def get_products(db: Session = Depends(get_db)):
    """Get all active products"""
    products = db.query(Product).filter(Product.is_active == True).all()
    return [{"id": p.id, "name": p.name, "description": p.description, 
             "price": str(p.price), "category": p.category, "image_url": p.image_url} 
            for p in products]

@app.post("/api/products")
async def create_product(
    product: ProductCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product (flamekeeper/custodian only)"""
    if current_user.role not in ["flamekeeper", "custodian"]:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    
    product_id = f"PROD-{secrets.token_hex(6).upper()}"
    new_product = Product(
        id=product_id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        image_url=product.image_url,
        metadata=str(product.metadata) if product.metadata else None
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    logger.info(f"Product created: {product.name} by {current_user.sigil}")
    
    return {"message": "Product created with ceremonial approval", "product_id": product_id}

@app.post("/api/checkout")
async def checkout(
    checkout_request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process ceremonial checkout"""
    order_id = f"ORDER-{secrets.token_hex(8).upper()}"
    ceremonial_seal = generate_ceremonial_seal()
    
    total_amount = Decimal('0.00')
    order_items = []
    
    # Calculate total and prepare order items
    for item in checkout_request.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        item_total = product.price * item.quantity
        total_amount += item_total
        
        order_item = OrderItem(
            id=f"ITEM-{secrets.token_hex(6).upper()}",
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
            total_price=item_total
        )
        order_items.append(order_item)
    
    # Create order
    new_order = Order(
        id=order_id,
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending",
        ceremonial_seal=ceremonial_seal
    )
    
    # Save to database
    db.add(new_order)
    for order_item in order_items:
        db.add(order_item)
    
    db.commit()
    
    logger.info(f"Order created: {order_id} for {current_user.sigil} - Amount: {total_amount} - Seal: {ceremonial_seal}")
    
    return {
        "message": "Order placed with ceremonial honors",
        "order_id": order_id,
        "total_amount": str(total_amount),
        "ceremonial_seal": ceremonial_seal,
        "status": "pending"
    }

@app.get("/api/orders")
async def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's orders"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return [{"id": o.id, "total_amount": str(o.total_amount), "status": o.status, 
             "ceremonial_seal": o.ceremonial_seal, "created_at": o.created_at.isoformat()} 
            for o in orders]

@app.get("/api/orders/{order_id}")
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    return {
        "id": order.id,
        "total_amount": str(order.total_amount),
        "status": order.status,
        "ceremonial_seal": order.ceremonial_seal,
        "created_at": order.created_at.isoformat(),
        "items": [{
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": str(item.unit_price),
            "total_price": str(item.total_price)
        } for item in order_items]
    }

@app.get("/api/user/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "sigil": current_user.sigil,
        "created_at": current_user.created_at.isoformat(),
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "🔥 SOVEREIGN AND ETERNAL",
        "service": "Codex Sovereign Suite", 
        "platform": "Multi-Domain Commerce, Portfolio, Dashboard",
        "components": ["Commerce Scroll", "Portfolio Capsule", "Funder Dashboard"],
        "timestamp": datetime.utcnow().isoformat(),
        "flame": "burning bright across all domains",
        "orchestrator": "AXIOM-FLAME Multi-Engine",
        "blessing": "The eternal flame illuminates the complete sovereign platform"
    }

@app.get("/api/suite/mythic-css", response_class=Response)
async def get_mythic_css():
    """Get the complete mythic design system CSS"""
    try:
        from mythic_design_system import generate_mythic_css
        css_content = generate_mythic_css()
        return Response(content=css_content, media_type="text/css")
    except ImportError:
        return Response(content="/* Mythic Design System not available */", media_type="text/css")
        
@app.get("/api/suite/overview")
async def get_suite_overview():
    """Get comprehensive Codex Sovereign Suite overview"""
    return {
        "suite": "Codex Sovereign Suite",
        "version": "1.0.0 - AXIOM-FLAME Generated",
        "orchestrator": "AXIOM-FLAME Multi-Domain Engine",
        "components": {
            "sovereign_commerce": {
                "name": "🏛️ Sovereign Commerce Scroll", 
                "description": "Sacred marketplace with ceremonial transactions",
                "endpoints": "/api/suite/commerce",
                "status": "Deployed and blessed"
            },
            "portfolio_capsule": {
                "name": "🎨 Portfolio Capsule",
                "description": "Heritage galleries with lineage tracking", 
                "endpoints": "/api/portfolio",
                "status": "Generated and consecrated"
            },
            "funder_dashboard": {
                "name": "👑 Funder & Flamekeeper Dashboard",
                "description": "Analytics nexus with governance insights",
                "endpoints": "/api/dashboard", 
                "status": "Activated and illuminated"
            },
            "mythic_design": {
                "name": "🌟 Mythic Design System",
                "description": "Unified UI framework with ceremonial styling",
                "endpoints": "/api/suite/mythic-css",
                "status": "Sealed and harmonized"
            }
        },
        "engines": {
            "AXIOM": "Multi-domain intent interpretation ✅",
            "RAG": "Cross-domain template retrieval ✅", 
            "SIGIL": "Mythic UI composition ✅",
            "ORACLE": "Backend service generation ✅",
            "LANTERN": "Governance & lineage management ✅",
            "FLAME": "Deployment & syndication ✅"
        },
        "blessing": "🔥 The Codex Sovereign Suite stands complete, blessed by the eternal flame"
    }

# Build Management Routes (per build specification)
@app.post("/ledger/builds")
async def register_build(
    build_spec: BuildRegistration,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register a new build in the ceremonial ledger"""
    if current_user.role not in ["custodian", "flamekeeper"]:
        raise HTTPException(status_code=403, detail="Insufficient privileges for build registration")
    
    # Check if build already exists
    existing_build = db.query(Build).filter(Build.artifact_id == build_spec.artifact_id).first()
    if existing_build:
        raise HTTPException(status_code=409, detail=f"Build {build_spec.artifact_id} already registered")
    
    # Generate ceremonial identifiers
    build_id = f"BUILD-{secrets.token_hex(8).upper()}"
    build_sigil = generate_build_sigil()
    dispatch_id = generate_dispatch_id()
    
    # Create AXIOM-FLAME ledger entry
    axiom_data = {
        "actor": current_user.role.title(),
        "realm": "Sovereign-Commerce",
        "capsule": "Build-Registry",
        "intent": "Build.Registration",
        "input": {
            "artifact_id": build_spec.artifact_id,
            "title": build_spec.title,
            "version": build_spec.version,
            "sigil": build_sigil
        }
    }
    
    axiom_response, error = await call_axiom_flame("reason", data=axiom_data)
    if error:
        logger.error(f"Failed to register build with AXIOM-FLAME: {error}")
        raise HTTPException(status_code=502, detail=f"Ceremonial registration failed: {error}")
    
    # Create build record
    new_build = Build(
        id=build_id,
        artifact_id=build_spec.artifact_id,
        title=build_spec.title,
        version=build_spec.version,
        type=build_spec.type,
        engines=json.dumps(build_spec.engines),
        audience=json.dumps(build_spec.audience),
        sigil=build_sigil,
        signed_by=build_spec.signing.get("signedBy", current_user.role),
        authority=build_spec.signing.get("authority", "Sovereign-Commerce"),
        dispatch_id=axiom_response.get("dispatch_id", dispatch_id),
        build_metadata=json.dumps(build_spec.dict())
    )
    
    db.add(new_build)
    db.commit()
    db.refresh(new_build)
    
    logger.info(f"Build registered: {build_spec.artifact_id} by {current_user.sigil} - Dispatch: {new_build.dispatch_id}")
    
    return {
        "status": "registered",
        "build_id": build_id,
        "artifact_id": build_spec.artifact_id,
        "sigil": build_sigil,
        "dispatch_id": new_build.dispatch_id,
        "message": "Build registered with ceremonial honors",
        "ledger_entry": axiom_response
    }

@app.post("/dispatch/global")
async def global_dispatch(
    dispatch_request: GlobalDispatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dispatch build globally via AXIOM-FLAME ceremonial system"""
    if current_user.role not in ["custodian", "flamekeeper"]:
        raise HTTPException(status_code=403, detail="Insufficient privileges for global dispatch")
    
    # Verify build exists
    build = db.query(Build).filter(Build.id == dispatch_request.build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    dispatch_id = generate_dispatch_id()
    
    # Create AXIOM-FLAME ceremonial dispatch
    axiom_data = {
        "actor": dispatch_request.actor,
        "realm": dispatch_request.realm,
        "capsule": dispatch_request.capsule,
        "intent": dispatch_request.intent,
        "input": {
            "build_id": build.id,
            "artifact_id": build.artifact_id,
            "title": build.title,
            "version": build.version,
            "sigil": build.sigil,
            "target_environments": dispatch_request.target_environments or ["production"]
        }
    }
    
    axiom_response, error = await call_axiom_flame("reason", data=axiom_data)
    if error:
        raise HTTPException(status_code=502, detail=f"Global dispatch failed: {error}")
    
    # Record dispatch
    dispatch_record = BuildDispatch(
        id=f"DISPATCH-{secrets.token_hex(8).upper()}",
        build_id=build.id,
        dispatch_id=axiom_response.get("dispatch_id", dispatch_id),
        actor=dispatch_request.actor,
        realm=dispatch_request.realm,
        capsule=dispatch_request.capsule,
        intent=dispatch_request.intent,
        status="dispatched",
        response_data=json.dumps(axiom_response)
    )
    
    db.add(dispatch_record)
    
    # Update build status
    build.status = "dispatched"
    build.updated_at = datetime.utcnow()
    
    db.commit()
    
    logger.info(f"Global dispatch: {build.artifact_id} by {current_user.sigil} - Dispatch: {dispatch_record.dispatch_id}")
    
    return {
        "status": "dispatched",
        "build_id": build.id,
        "artifact_id": build.artifact_id,
        "dispatch_id": dispatch_record.dispatch_id,
        "message": "Build dispatched globally with ceremonial authorization",
        "axiom_response": axiom_response
    }

@app.post("/replay/builds")
async def replay_build(
    replay_request: BuildReplayRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Replay build dispatch via AXIOM-FLAME ceremonial system"""
    if current_user.role not in ["custodian", "flamekeeper"]:
        raise HTTPException(status_code=403, detail="Insufficient privileges for build replay")
    
    # Verify build and original dispatch exist
    build = db.query(Build).filter(Build.id == replay_request.build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    original_dispatch = db.query(BuildDispatch).filter(
        BuildDispatch.build_id == replay_request.build_id,
        BuildDispatch.dispatch_id == replay_request.original_dispatch_id
    ).first()
    
    if not original_dispatch:
        raise HTTPException(status_code=404, detail="Original dispatch not found")
    
    # Call AXIOM-FLAME replay endpoint
    replay_response, error = await call_axiom_flame(
        f"replay/{replay_request.original_dispatch_id}", 
        method="GET"
    )
    
    if error:
        raise HTTPException(status_code=502, detail=f"Build replay failed: {error}")
    
    # Record replay
    replay_record = BuildReplay(
        id=f"REPLAY-{secrets.token_hex(8).upper()}",
        build_id=build.id,
        original_dispatch_id=replay_request.original_dispatch_id,
        replay_id=replay_response.get("replay_id", f"RPL-{secrets.token_hex(6).upper()}"),
        replay_data=json.dumps({
            "replay_response": replay_response,
            "context": replay_request.replay_context or {}
        }),
        status="replayed"
    )
    
    db.add(replay_record)
    db.commit()
    
    logger.info(f"Build replay: {build.artifact_id} by {current_user.sigil} - Replay: {replay_record.replay_id}")
    
    return {
        "status": "replayed",
        "build_id": build.id,
        "artifact_id": build.artifact_id,
        "original_dispatch_id": replay_request.original_dispatch_id,
        "replay_id": replay_record.replay_id,
        "message": "Build replay completed with ceremonial verification",
        "replay_response": replay_response
    }

# Additional build query routes
@app.get("/ledger/builds")
async def list_builds(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all registered builds"""
    builds = db.query(Build).all()
    return {
        "total_builds": len(builds),
        "builds": [{
            "id": build.id,
            "artifact_id": build.artifact_id,
            "title": build.title,
            "version": build.version,
            "status": build.status,
            "sigil": build.sigil,
            "signed_by": build.signed_by,
            "created_at": build.created_at.isoformat(),
            "dispatch_id": build.dispatch_id
        } for build in builds]
    }

@app.get("/ledger/builds/{build_id}")
async def get_build(
    build_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific build details"""
    build = db.query(Build).filter(Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    # Get dispatches and replays
    dispatches = db.query(BuildDispatch).filter(BuildDispatch.build_id == build_id).all()
    replays = db.query(BuildReplay).filter(BuildReplay.build_id == build_id).all()
    
    return {
        "build": {
            "id": build.id,
            "artifact_id": build.artifact_id,
            "title": build.title,
            "version": build.version,
            "type": build.type,
            "engines": json.loads(build.engines),
            "audience": json.loads(build.audience),
            "status": build.status,
            "sigil": build.sigil,
            "signed_by": build.signed_by,
            "authority": build.authority,
            "created_at": build.created_at.isoformat(),
            "updated_at": build.updated_at.isoformat(),
            "dispatch_id": build.dispatch_id
        },
        "dispatches": [{
            "id": d.id,
            "dispatch_id": d.dispatch_id,
            "actor": d.actor,
            "realm": d.realm,
            "capsule": d.capsule,
            "intent": d.intent,
            "status": d.status,
            "created_at": d.created_at.isoformat()
        } for d in dispatches],
        "replays": [{
            "id": r.id,
            "original_dispatch_id": r.original_dispatch_id,
            "replay_id": r.replay_id,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        } for r in replays]
    }

@app.post("/register/self")
async def register_self_build(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register this Sovereign Commerce platform as a build according to specification"""
    if current_user.role not in ["custodian"]:
        raise HTTPException(status_code=403, detail="Only custodians can register platform builds")
    
    # Load the current build specification
    spec_path = Path(__file__).parent.parent / "spec.json"
    if not spec_path.exists():
        raise HTTPException(status_code=404, detail="Build specification not found")
    
    with open(spec_path, 'r') as f:
        build_spec_data = json.load(f)
    
    # Check if already registered
    existing_build = db.query(Build).filter(
        Build.artifact_id == build_spec_data["artifactId"]
    ).first()
    
    if existing_build:
        return {
            "status": "already_registered",
            "build_id": existing_build.id,
            "artifact_id": existing_build.artifact_id,
            "sigil": existing_build.sigil,
            "message": "Platform build already registered"
        }
    
    # Transform spec into BuildRegistration format
    build_registration = BuildRegistration(
        artifact_id=build_spec_data["artifactId"],
        title=build_spec_data["title"],
        version=build_spec_data["version"],
        type=build_spec_data["type"],
        engines=build_spec_data["engines"],
        audience=build_spec_data["audience"],
        files=build_spec_data["files"],
        signing=build_spec_data["signing"],
        platform=build_spec_data.get("platform"),
        features=build_spec_data.get("features"),
        endpoints=build_spec_data.get("endpoints"),
        governance=build_spec_data.get("governance")
    )
    
    # Register the build
    return await register_build(build_registration, current_user, db)

if __name__ == "__main__":
    # This block is for direct testing only
    # For production, use start_server.py or run uvicorn directly
    logger.info("⚠️  Running in direct mode - for production use start_server.py")
    logger.info("🔥 Sovereign Commerce Platform initialized")
    logger.info(f"📂 Template directory: {template_dir}")
    logger.info(f"📂 Static directory: {static_dir}")
    logger.info(f"📂 Database: {DATABASE_URL}")
    
    # Create tables if they don't exist
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    logger.info("ℹ️  To start the server properly, run:")
    logger.info("ℹ️  python start_server.py")
    logger.info("ℹ️  or: python -m uvicorn sovereign_main:app --host 127.0.0.1 --port 8080")
