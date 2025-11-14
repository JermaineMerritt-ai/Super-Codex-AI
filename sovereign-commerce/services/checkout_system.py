#!/usr/bin/env python3
"""
Advanced Checkout System for Diaspora Funders
Ceremonial purchase flows with sovereign recognition and community support

Built with dignity for the diaspora funder experience.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from decimal import Decimal
import json
import secrets
import asyncio
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, DECIMAL, Integer, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sovereign_main import Base, User, Product, Order, OrderItem, SessionLocal

# Logging setup
logger = logging.getLogger(__name__)

# Checkout-specific Models
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    payment_type = Column(String)  # ceremonial, traditional, crypto, solidarity
    cultural_context = Column(Text)  # Cultural significance of payment method
    is_active = Column(Boolean, default=True)
    requires_verification = Column(Boolean, default=False)
    sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CheckoutSession(Base):
    __tablename__ = "checkout_sessions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    session_token = Column(String, unique=True)
    cart_data = Column(Text)  # JSON cart contents
    shipping_address = Column(Text)  # JSON address data
    payment_method_id = Column(String, ForeignKey('payment_methods.id'))
    cultural_preferences = Column(Text)  # JSON cultural preferences
    community_fund_contribution = Column(DECIMAL(10, 2), default=0)
    total_amount = Column(DECIMAL(10, 2))
    status = Column(String)  # active, abandoned, completed, expired
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class CommunityFund(Base):
    __tablename__ = "community_funds"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    fund_name = Column(String, unique=True, index=True)
    description = Column(Text)
    target_region = Column(String)  # Diaspora region this fund supports
    total_contributions = Column(DECIMAL(10, 2), default=0)
    current_goal = Column(DECIMAL(10, 2))
    fund_purpose = Column(Text)  # What the fund supports
    managed_by = Column(String, ForeignKey('users.id'))
    sigil = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class FundContribution(Base):
    __tablename__ = "fund_contributions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    fund_id = Column(String, ForeignKey('community_funds.id'))
    order_id = Column(String, ForeignKey('orders.id'))
    user_id = Column(String, ForeignKey('users.id'))
    contribution_amount = Column(DECIMAL(10, 2))
    contribution_percentage = Column(DECIMAL(5, 2))  # Percentage of order total
    ceremonial_seal = Column(String)
    cultural_note = Column(Text)  # User's note about their contribution
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderCeremony(Base):
    __tablename__ = "order_ceremonies"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey('orders.id'), unique=True)
    ceremony_type = Column(String)  # blessing, recognition, dedication
    cultural_elements = Column(Text)  # JSON cultural ceremony data
    community_witnesses = Column(Text)  # JSON list of community members
    ceremonial_blessing = Column(Text)  # Custom blessing or dedication
    ceremony_sigil = Column(String, unique=True)
    performed_by = Column(String, ForeignKey('users.id'))
    performed_at = Column(DateTime, default=datetime.utcnow)
    is_completed = Column(Boolean, default=False)

class OrderStatus(str, Enum):
    """Enhanced order status for ceremonial tracking"""
    CART = "cart"
    INITIATED = "initiated"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_CONFIRMED = "payment_confirmed"
    CEREMONY_PREPARED = "ceremony_prepared"
    BLESSED = "blessed"
    FULFILLED = "fulfilled"
    HONORED = "honored"
    COMMUNITY_RECOGNIZED = "community_recognized"

# Advanced Checkout Service
class DiasporaCheckoutService:
    """Advanced checkout service with ceremonial features for diaspora funders"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
        self.session_timeout_hours = 24  # Checkout sessions valid for 24 hours
    
    def create_payment_method(self, name: str, description: str, payment_type: str,
                            cultural_context: str, requires_verification: bool = False) -> Dict:
        """Create a new payment method with cultural context"""
        # Check for existing payment method
        existing = self.db.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Payment method '{name}' already exists")
        
        method_id = f"PAY-{secrets.token_hex(6).upper()}"
        method_sigil = f"SIGIL-PAY-{secrets.token_hex(4).upper()}"
        
        payment_method = PaymentMethod(
            id=method_id,
            name=name,
            description=description,
            payment_type=payment_type,
            cultural_context=cultural_context,
            requires_verification=requires_verification,
            sigil=method_sigil
        )
        
        self.db.add(payment_method)
        self.db.commit()
        self.db.refresh(payment_method)
        
        self.logger.info(f"Payment method created: {name} with sigil {method_sigil}")
        
        return {
            "payment_method_id": method_id,
            "name": name,
            "sigil": method_sigil,
            "message": "Payment method created with ceremonial recognition"
        }
    
    def create_community_fund(self, fund_name: str, description: str, target_region: str,
                            current_goal: Decimal, fund_purpose: str, manager_id: str) -> Dict:
        """Create a community fund for diaspora support"""
        # Verify manager exists and has appropriate role
        manager = self.db.query(User).filter(User.id == manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Fund manager not found")
        
        if manager.role not in ["flamekeeper", "custodian"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges to manage community funds")
        
        # Check for existing fund
        existing_fund = self.db.query(CommunityFund).filter(
            CommunityFund.fund_name == fund_name
        ).first()
        if existing_fund:
            raise HTTPException(status_code=409, detail=f"Fund '{fund_name}' already exists")
        
        fund_id = f"FUND-{secrets.token_hex(6).upper()}"
        fund_sigil = f"SIGIL-FUND-{secrets.token_hex(4).upper()}"
        
        community_fund = CommunityFund(
            id=fund_id,
            fund_name=fund_name,
            description=description,
            target_region=target_region,
            current_goal=current_goal,
            fund_purpose=fund_purpose,
            managed_by=manager_id,
            sigil=fund_sigil
        )
        
        self.db.add(community_fund)
        self.db.commit()
        self.db.refresh(community_fund)
        
        self.logger.info(f"Community fund created: {fund_name} for {target_region} with goal ${current_goal}")
        
        return {
            "fund_id": fund_id,
            "fund_name": fund_name,
            "target_region": target_region,
            "sigil": fund_sigil,
            "message": "Community fund created with ceremonial honors"
        }
    
    def initialize_checkout_session(self, user_id: str, cart_items: List[Dict],
                                  cultural_preferences: Dict = None) -> Dict:
        """Initialize a checkout session with cultural preferences"""
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate total amount from cart items
        total_amount = Decimal('0.00')
        validated_cart = []
        
        for item in cart_items:
            product = self.db.query(Product).filter(Product.id == item['product_id']).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")
            
            if not product.is_active:
                raise HTTPException(status_code=400, detail=f"Product {product.name} is not available")
            
            if item['quantity'] <= 0:
                raise HTTPException(status_code=400, detail="Invalid quantity")
            
            item_total = product.price * item['quantity']
            total_amount += item_total
            
            validated_cart.append({
                "product_id": item['product_id'],
                "product_name": product.name,
                "quantity": item['quantity'],
                "unit_price": str(product.price),
                "total_price": str(item_total)
            })
        
        # Create checkout session
        session_id = f"CHECKOUT-{secrets.token_hex(8).upper()}"
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=self.session_timeout_hours)
        
        checkout_session = CheckoutSession(
            id=session_id,
            user_id=user_id,
            session_token=session_token,
            cart_data=json.dumps(validated_cart),
            cultural_preferences=json.dumps(cultural_preferences) if cultural_preferences else None,
            total_amount=total_amount,
            status="active",
            expires_at=expires_at
        )
        
        self.db.add(checkout_session)
        self.db.commit()
        self.db.refresh(checkout_session)
        
        self.logger.info(f"Checkout session initialized: {session_id} for user {user.sigil}")
        
        return {
            "session_id": session_id,
            "session_token": session_token,
            "total_amount": str(total_amount),
            "cart_items": validated_cart,
            "expires_at": expires_at.isoformat(),
            "cultural_preferences": cultural_preferences,
            "message": "Checkout session initialized with cultural honors"
        }
    
    def update_checkout_session(self, session_id: str, session_token: str,
                              shipping_address: Dict = None, payment_method_id: str = None,
                              community_fund_contribution: Decimal = None) -> Dict:
        """Update checkout session with shipping and payment details"""
        # Verify session
        session = self.db.query(CheckoutSession).filter(
            CheckoutSession.id == session_id,
            CheckoutSession.session_token == session_token,
            CheckoutSession.status == "active"
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Invalid checkout session")
        
        if datetime.utcnow() > session.expires_at:
            session.status = "expired"
            self.db.commit()
            raise HTTPException(status_code=410, detail="Checkout session has expired")
        
        # Update fields if provided
        if shipping_address:
            session.shipping_address = json.dumps(shipping_address)
        
        if payment_method_id:
            # Verify payment method exists
            payment_method = self.db.query(PaymentMethod).filter(
                PaymentMethod.id == payment_method_id,
                PaymentMethod.is_active == True
            ).first()
            if not payment_method:
                raise HTTPException(status_code=404, detail="Payment method not found")
            
            session.payment_method_id = payment_method_id
        
        if community_fund_contribution is not None:
            if community_fund_contribution < 0:
                raise HTTPException(status_code=400, detail="Community fund contribution cannot be negative")
            session.community_fund_contribution = community_fund_contribution
        
        self.db.commit()
        self.db.refresh(session)
        
        return {
            "session_id": session_id,
            "status": "updated",
            "shipping_address": json.loads(session.shipping_address) if session.shipping_address else None,
            "payment_method_id": session.payment_method_id,
            "community_fund_contribution": str(session.community_fund_contribution),
            "message": "Checkout session updated with ceremonial recognition"
        }
    
    def complete_ceremonial_checkout(self, session_id: str, session_token: str,
                                   ceremony_preferences: Dict = None,
                                   selected_fund_id: str = None) -> Dict:
        """Complete the ceremonial checkout process"""
        # Verify session
        session = self.db.query(CheckoutSession).filter(
            CheckoutSession.id == session_id,
            CheckoutSession.session_token == session_token,
            CheckoutSession.status == "active"
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Invalid checkout session")
        
        if datetime.utcnow() > session.expires_at:
            session.status = "expired"
            self.db.commit()
            raise HTTPException(status_code=410, detail="Checkout session has expired")
        
        # Verify required information is present
        if not session.payment_method_id:
            raise HTTPException(status_code=400, detail="Payment method not selected")
        
        # Create the order
        order_id = f"ORDER-{secrets.token_hex(8).upper()}"
        ceremonial_seal = self._generate_ceremonial_seal()
        
        cart_items = json.loads(session.cart_data)
        final_total = session.total_amount + session.community_fund_contribution
        
        new_order = Order(
            id=order_id,
            user_id=session.user_id,
            total_amount=final_total,
            status=OrderStatus.INITIATED.value,
            ceremonial_seal=ceremonial_seal
        )
        
        self.db.add(new_order)
        
        # Create order items
        order_items = []
        for cart_item in cart_items:
            item_id = f"ITEM-{secrets.token_hex(6).upper()}"
            order_item = OrderItem(
                id=item_id,
                order_id=order_id,
                product_id=cart_item['product_id'],
                quantity=cart_item['quantity'],
                unit_price=Decimal(cart_item['unit_price']),
                total_price=Decimal(cart_item['total_price'])
            )
            order_items.append(order_item)
            self.db.add(order_item)
        
        # Handle community fund contribution if specified
        if session.community_fund_contribution > 0 and selected_fund_id:
            fund_contribution = self._create_fund_contribution(
                fund_id=selected_fund_id,
                order_id=order_id,
                user_id=session.user_id,
                contribution_amount=session.community_fund_contribution,
                order_total=session.total_amount
            )
        
        # Create order ceremony if ceremony preferences provided
        if ceremony_preferences:
            ceremony_id = self._create_order_ceremony(
                order_id=order_id,
                user_id=session.user_id,
                ceremony_preferences=ceremony_preferences
            )
        
        # Mark session as completed
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        
        self.db.commit()
        
        self.logger.info(f"Ceremonial checkout completed: Order {order_id} with seal {ceremonial_seal}")
        
        return {
            "order_id": order_id,
            "ceremonial_seal": ceremonial_seal,
            "total_amount": str(final_total),
            "community_contribution": str(session.community_fund_contribution),
            "order_items": cart_items,
            "status": OrderStatus.INITIATED.value,
            "ceremony_id": ceremony_id if ceremony_preferences else None,
            "message": "Order completed with ceremonial honors and community recognition"
        }
    
    def get_available_payment_methods(self, payment_type_filter: str = None) -> Dict:
        """Get available payment methods with cultural context"""
        query = self.db.query(PaymentMethod).filter(PaymentMethod.is_active == True)
        
        if payment_type_filter:
            query = query.filter(PaymentMethod.payment_type == payment_type_filter)
        
        payment_methods = query.all()
        
        return {
            "total_methods": len(payment_methods),
            "payment_methods": [{
                "id": method.id,
                "name": method.name,
                "description": method.description,
                "payment_type": method.payment_type,
                "cultural_context": method.cultural_context,
                "requires_verification": method.requires_verification,
                "sigil": method.sigil
            } for method in payment_methods],
            "filter": payment_type_filter,
            "message": "Available payment methods with cultural context"
        }
    
    def get_community_funds(self, target_region: str = None) -> Dict:
        """Get community funds available for contributions"""
        query = self.db.query(CommunityFund).filter(CommunityFund.is_active == True)
        
        if target_region:
            query = query.filter(CommunityFund.target_region == target_region)
        
        funds = query.all()
        
        funds_with_progress = []
        for fund in funds:
            # Calculate progress towards goal
            progress_percentage = 0
            if fund.current_goal > 0:
                progress_percentage = min(
                    float(fund.total_contributions / fund.current_goal) * 100,
                    100
                )
            
            funds_with_progress.append({
                "id": fund.id,
                "fund_name": fund.fund_name,
                "description": fund.description,
                "target_region": fund.target_region,
                "total_contributions": str(fund.total_contributions),
                "current_goal": str(fund.current_goal),
                "progress_percentage": round(progress_percentage, 1),
                "fund_purpose": fund.fund_purpose,
                "sigil": fund.sigil,
                "created_at": fund.created_at.isoformat()
            })
        
        return {
            "total_funds": len(funds_with_progress),
            "community_funds": funds_with_progress,
            "target_region": target_region,
            "message": "Community funds available for diaspora support"
        }
    
    def get_checkout_session_status(self, session_id: str, session_token: str) -> Dict:
        """Get current checkout session status"""
        session = self.db.query(CheckoutSession).filter(
            CheckoutSession.id == session_id,
            CheckoutSession.session_token == session_token
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Checkout session not found")
        
        # Check if expired
        is_expired = datetime.utcnow() > session.expires_at
        if is_expired and session.status == "active":
            session.status = "expired"
            self.db.commit()
        
        return {
            "session_id": session_id,
            "status": session.status,
            "total_amount": str(session.total_amount),
            "cart_items": json.loads(session.cart_data) if session.cart_data else [],
            "community_fund_contribution": str(session.community_fund_contribution),
            "expires_at": session.expires_at.isoformat(),
            "is_expired": is_expired,
            "time_remaining_hours": max(0, (session.expires_at - datetime.utcnow()).total_seconds() / 3600),
            "message": "Checkout session status with ceremonial details"
        }
    
    def _generate_ceremonial_seal(self) -> str:
        """Generate a ceremonial seal for orders"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"SEAL-{timestamp}-{secrets.token_hex(4).upper()}"
    
    def _create_fund_contribution(self, fund_id: str, order_id: str, user_id: str,
                                contribution_amount: Decimal, order_total: Decimal) -> str:
        """Create a fund contribution record"""
        # Verify fund exists
        fund = self.db.query(CommunityFund).filter(CommunityFund.id == fund_id).first()
        if not fund:
            raise HTTPException(status_code=404, detail="Community fund not found")
        
        contribution_id = f"CONTRIB-{secrets.token_hex(6).upper()}"
        contribution_percentage = (contribution_amount / order_total) * 100 if order_total > 0 else 0
        contribution_seal = f"SEAL-CONTRIB-{secrets.token_hex(4).upper()}"
        
        fund_contribution = FundContribution(
            id=contribution_id,
            fund_id=fund_id,
            order_id=order_id,
            user_id=user_id,
            contribution_amount=contribution_amount,
            contribution_percentage=contribution_percentage,
            ceremonial_seal=contribution_seal
        )
        
        self.db.add(fund_contribution)
        
        # Update fund total
        fund.total_contributions += contribution_amount
        
        self.logger.info(f"Fund contribution created: {contribution_amount} to {fund.fund_name}")
        
        return contribution_id
    
    def _create_order_ceremony(self, order_id: str, user_id: str, ceremony_preferences: Dict) -> str:
        """Create an order ceremony record"""
        ceremony_id = f"CEREMONY-{secrets.token_hex(6).upper()}"
        ceremony_sigil = f"SIGIL-CEREMONY-{secrets.token_hex(4).upper()}"
        
        order_ceremony = OrderCeremony(
            id=ceremony_id,
            order_id=order_id,
            ceremony_type=ceremony_preferences.get("type", "blessing"),
            cultural_elements=json.dumps(ceremony_preferences.get("cultural_elements", {})),
            community_witnesses=json.dumps(ceremony_preferences.get("witnesses", [])),
            ceremonial_blessing=ceremony_preferences.get("blessing", ""),
            ceremony_sigil=ceremony_sigil,
            performed_by=user_id
        )
        
        self.db.add(order_ceremony)
        
        self.logger.info(f"Order ceremony created: {ceremony_id} for order {order_id}")
        
        return ceremony_id

def get_diaspora_checkout_service(db: Session = None) -> DiasporaCheckoutService:
    """Get diaspora checkout service instance"""
    if db is None:
        db = SessionLocal()
    return DiasporaCheckoutService(db)

# Utility functions for seeding data
def seed_payment_methods(db: Session):
    """Seed default payment methods with cultural context"""
    checkout_service = DiasporaCheckoutService(db)
    
    payment_methods = [
        {
            "name": "Ceremonial Tribute",
            "description": "Traditional offering system based on community reciprocity",
            "payment_type": "ceremonial",
            "cultural_context": "Ancient practice of mutual aid and community support through symbolic exchange"
        },
        {
            "name": "Solidarity Fund Transfer",
            "description": "Direct transfers between diaspora community members",
            "payment_type": "solidarity",
            "cultural_context": "Peer-to-peer financial support reflecting diaspora mutual aid traditions"
        },
        {
            "name": "Digital Sovereignty Coin",
            "description": "Cryptocurrency for autonomous financial transactions",
            "payment_type": "crypto",
            "cultural_context": "Blockchain-based currency promoting financial independence from traditional systems"
        },
        {
            "name": "Heritage Credit Union",
            "description": "Banking cooperative focused on diaspora communities",
            "payment_type": "traditional",
            "cultural_context": "Community-owned financial institutions serving diaspora banking needs"
        }
    ]
    
    for method_data in payment_methods:
        try:
            checkout_service.create_payment_method(
                name=method_data["name"],
                description=method_data["description"],
                payment_type=method_data["payment_type"],
                cultural_context=method_data["cultural_context"]
            )
            logger.info(f"Payment method created: {method_data['name']}")
        except HTTPException as e:
            if "already exists" in str(e.detail):
                logger.info(f"Payment method already exists: {method_data['name']}")
            else:
                logger.error(f"Error creating payment method {method_data['name']}: {e.detail}")
        except Exception as e:
            logger.error(f"Unexpected error creating payment method {method_data['name']}: {e}")

def seed_community_funds(db: Session, manager_id: str):
    """Seed sample community funds"""
    checkout_service = DiasporaCheckoutService(db)
    
    community_funds = [
        {
            "fund_name": "African Diaspora Educational Fund",
            "description": "Supporting educational initiatives in African diaspora communities",
            "target_region": "African Diaspora",
            "current_goal": Decimal('10000.00'),
            "fund_purpose": "Scholarships, educational resources, and cultural preservation programs"
        },
        {
            "fund_name": "Latin American Solidarity Network",
            "description": "Emergency support and community development for Latin American diaspora",
            "target_region": "Latin American Diaspora",
            "current_goal": Decimal('15000.00'),
            "fund_purpose": "Crisis response, legal aid, and community organizing resources"
        },
        {
            "fund_name": "Asian Heritage Preservation Initiative",
            "description": "Preserving and promoting Asian diaspora cultural heritage",
            "target_region": "Asian Diaspora",
            "current_goal": Decimal('8000.00'),
            "fund_purpose": "Cultural events, language preservation, and intergenerational programs"
        },
        {
            "fund_name": "Global Digital Nomad Support",
            "description": "Supporting location-independent diaspora communities",
            "target_region": "Digital Nomad",
            "current_goal": Decimal('12000.00'),
            "fund_purpose": "Technology infrastructure, co-working spaces, and virtual community building"
        }
    ]
    
    for fund_data in community_funds:
        try:
            result = checkout_service.create_community_fund(
                fund_name=fund_data["fund_name"],
                description=fund_data["description"],
                target_region=fund_data["target_region"],
                current_goal=fund_data["current_goal"],
                fund_purpose=fund_data["fund_purpose"],
                manager_id=manager_id
            )
            logger.info(f"Community fund created: {fund_data['fund_name']} - {result['fund_id']}")
        except Exception as e:
            logger.error(f"Error creating fund {fund_data['fund_name']}: {e}")

if __name__ == "__main__":
    # Test the checkout service
    from sovereign_main import engine, SessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Test with a session
    db = SessionLocal()
    
    try:
        # Seed sample data
        seed_payment_methods(db)
        
        # Create test manager (you'll need to provide a real user ID in practice)
        test_manager_id = "USER-TEST-MANAGER"
        seed_community_funds(db, test_manager_id)
        
        # Test checkout initialization
        checkout_service = DiasporaCheckoutService(db)
        
        # Test cart items
        test_cart = [
            {"product_id": "PROD-TEST1", "quantity": 1},
            {"product_id": "PROD-TEST2", "quantity": 2}
        ]
        
        # This would fail without real products, but shows the structure
        print("Checkout service initialized successfully")
        
        # Get payment methods
        payment_methods = checkout_service.get_available_payment_methods()
        print("Payment methods:", json.dumps(payment_methods, indent=2, default=str))
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        db.close()