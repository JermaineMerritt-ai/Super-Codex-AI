#!/usr/bin/env python3
"""
Enhanced Product Catalog for Diaspora Funders
Sacred offerings with cultural significance and sovereign recognition

Built with ceremonial dignity for the diaspora community.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from decimal import Decimal
from pathlib import Path
import json
import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, DECIMAL, Integer, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sovereign_main import Base, User, Product, SessionLocal

# Logging setup
logger = logging.getLogger(__name__)

# Enhanced Product Models
class ProductCategory(Base):
    __tablename__ = "product_categories"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    cultural_significance = Column(Text)  # Cultural context for diaspora
    sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'))
    attribute_type = Column(String)  # cultural, ceremonial, functional
    attribute_name = Column(String)
    attribute_value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductReview(Base):
    __tablename__ = "product_reviews"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'))
    user_id = Column(String, ForeignKey('users.id'))
    rating = Column(Integer)  # 1-5 scale
    review_text = Column(Text)
    cultural_context = Column(Text)  # Cultural significance comments
    ceremonial_seal = Column(String)  # Unique review seal
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)

class CulturalCollection(Base):
    __tablename__ = "cultural_collections"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    diaspora_region = Column(String)  # Geographic or cultural region
    curator_id = Column(String, ForeignKey('users.id'))
    sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_featured = Column(Boolean, default=False)
    metadata_json = Column(Text)  # JSON for additional cultural data

class ProductCollection(Base):
    __tablename__ = "product_collections"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey('products.id'))
    collection_id = Column(String, ForeignKey('cultural_collections.id'))
    display_order = Column(Integer, default=0)
    cultural_notes = Column(Text)
    added_at = Column(DateTime, default=datetime.utcnow)

# Enhanced Product Catalog Service
class DiasporaProductCatalog:
    """Enhanced product catalog service for diaspora funders"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
    
    def create_category(self, name: str, description: str, cultural_significance: str, creator_role: str) -> Dict:
        """Create a new product category with cultural context"""
        if creator_role not in ["flamekeeper", "custodian"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges for category creation")
        
        # Check for existing category
        existing_category = self.db.query(ProductCategory).filter(
            ProductCategory.name == name
        ).first()
        
        if existing_category:
            raise HTTPException(status_code=409, detail=f"Category '{name}' already exists")
        
        category_id = f"CAT-{secrets.token_hex(6).upper()}"
        category_sigil = f"SIGIL-CAT-{secrets.token_hex(4).upper()}"
        
        new_category = ProductCategory(
            id=category_id,
            name=name,
            description=description,
            cultural_significance=cultural_significance,
            sigil=category_sigil
        )
        
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        
        self.logger.info(f"Category created: {name} with sigil {category_sigil}")
        
        return {
            "category_id": category_id,
            "name": name,
            "sigil": category_sigil,
            "message": "Category created with cultural honors"
        }
    
    def create_cultural_collection(self, name: str, description: str, diaspora_region: str, 
                                  curator_id: str, metadata: Dict = None) -> Dict:
        """Create a cultural collection curated for specific diaspora regions"""
        collection_id = f"COLL-{secrets.token_hex(6).upper()}"
        collection_sigil = f"SIGIL-COLL-{secrets.token_hex(4).upper()}"
        
        new_collection = CulturalCollection(
            id=collection_id,
            name=name,
            description=description,
            diaspora_region=diaspora_region,
            curator_id=curator_id,
            sigil=collection_sigil,
            metadata_json=json.dumps(metadata) if metadata else None
        )
        
        self.db.add(new_collection)
        self.db.commit()
        self.db.refresh(new_collection)
        
        self.logger.info(f"Cultural collection created: {name} for region {diaspora_region}")
        
        return {
            "collection_id": collection_id,
            "name": name,
            "diaspora_region": diaspora_region,
            "sigil": collection_sigil,
            "message": "Cultural collection created with ceremonial honors"
        }
    
    def add_product_to_collection(self, product_id: str, collection_id: str, 
                                 cultural_notes: str = None, display_order: int = 0) -> Dict:
        """Add a product to a cultural collection"""
        # Verify product and collection exist
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        collection = self.db.query(CulturalCollection).filter(
            CulturalCollection.id == collection_id
        ).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        # Check if already in collection
        existing = self.db.query(ProductCollection).filter(
            ProductCollection.product_id == product_id,
            ProductCollection.collection_id == collection_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=409, detail="Product already in collection")
        
        pc_id = f"PC-{secrets.token_hex(6).upper()}"
        product_collection = ProductCollection(
            id=pc_id,
            product_id=product_id,
            collection_id=collection_id,
            cultural_notes=cultural_notes,
            display_order=display_order
        )
        
        self.db.add(product_collection)
        self.db.commit()
        
        self.logger.info(f"Product {product_id} added to collection {collection_id}")
        
        return {
            "message": "Product added to cultural collection",
            "product_name": product.name,
            "collection_name": collection.name,
            "cultural_notes": cultural_notes
        }
    
    def add_product_attribute(self, product_id: str, attribute_type: str, 
                            attribute_name: str, attribute_value: str) -> Dict:
        """Add cultural or ceremonial attributes to products"""
        # Verify product exists
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        attr_id = f"ATTR-{secrets.token_hex(6).upper()}"
        product_attribute = ProductAttribute(
            id=attr_id,
            product_id=product_id,
            attribute_type=attribute_type,
            attribute_name=attribute_name,
            attribute_value=attribute_value
        )
        
        self.db.add(product_attribute)
        self.db.commit()
        
        self.logger.info(f"Attribute added to product {product_id}: {attribute_name}")
        
        return {
            "attribute_id": attr_id,
            "attribute_type": attribute_type,
            "attribute_name": attribute_name,
            "message": "Product attribute added with ceremonial recognition"
        }
    
    def create_product_review(self, product_id: str, user_id: str, rating: int, 
                            review_text: str, cultural_context: str = None) -> Dict:
        """Create a product review with cultural context"""
        # Verify product exists
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        review_id = f"REV-{secrets.token_hex(6).upper()}"
        ceremonial_seal = f"SEAL-REV-{secrets.token_hex(4).upper()}"
        
        product_review = ProductReview(
            id=review_id,
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            review_text=review_text,
            cultural_context=cultural_context,
            ceremonial_seal=ceremonial_seal
        )
        
        self.db.add(product_review)
        self.db.commit()
        
        self.logger.info(f"Review created for product {product_id} by user {user_id}")
        
        return {
            "review_id": review_id,
            "ceremonial_seal": ceremonial_seal,
            "rating": rating,
            "message": "Review created with cultural honors"
        }
    
    def get_enhanced_product_catalog(self, category_filter: str = None, 
                                   diaspora_region: str = None, 
                                   cultural_significance: str = None) -> Dict:
        """Get enhanced product catalog with cultural context"""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        # Apply category filter
        if category_filter:
            category = self.db.query(ProductCategory).filter(
                ProductCategory.name == category_filter
            ).first()
            if category:
                query = query.filter(Product.category == category.name)
        
        products = query.all()
        enhanced_products = []
        
        for product in products:
            # Get attributes
            attributes = self.db.query(ProductAttribute).filter(
                ProductAttribute.product_id == product.id
            ).all()
            
            # Get reviews and average rating
            reviews = self.db.query(ProductReview).filter(
                ProductReview.product_id == product.id
            ).all()
            
            avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            
            # Get cultural collections this product belongs to
            collections = self.db.query(CulturalCollection).join(
                ProductCollection, CulturalCollection.id == ProductCollection.collection_id
            ).filter(ProductCollection.product_id == product.id).all()
            
            # Filter by diaspora region if specified
            if diaspora_region:
                region_collections = [c for c in collections if c.diaspora_region == diaspora_region]
                if not region_collections:
                    continue
            
            enhanced_product = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "currency": product.currency,
                "category": product.category,
                "image_url": product.image_url,
                "average_rating": round(avg_rating, 1),
                "review_count": len(reviews),
                "attributes": {
                    attr.attribute_name: {
                        "type": attr.attribute_type,
                        "value": attr.attribute_value
                    } for attr in attributes
                },
                "cultural_collections": [{
                    "name": coll.name,
                    "diaspora_region": coll.diaspora_region,
                    "sigil": coll.sigil
                } for coll in collections],
                "created_at": product.created_at.isoformat()
            }
            
            enhanced_products.append(enhanced_product)
        
        # Get featured collections
        featured_collections = self.db.query(CulturalCollection).filter(
            CulturalCollection.is_featured == True
        ).all()
        
        # Get categories with cultural significance
        categories = self.db.query(ProductCategory).filter(
            ProductCategory.is_active == True
        ).all()
        
        return {
            "total_products": len(enhanced_products),
            "products": enhanced_products,
            "featured_collections": [{
                "id": coll.id,
                "name": coll.name,
                "description": coll.description,
                "diaspora_region": coll.diaspora_region,
                "sigil": coll.sigil
            } for coll in featured_collections],
            "categories": [{
                "id": cat.id,
                "name": cat.name,
                "description": cat.description,
                "cultural_significance": cat.cultural_significance,
                "sigil": cat.sigil
            } for cat in categories],
            "filters": {
                "category": category_filter,
                "diaspora_region": diaspora_region,
                "cultural_significance": cultural_significance
            },
            "message": "Enhanced catalog with cultural context"
        }
    
    def get_product_with_cultural_context(self, product_id: str) -> Dict:
        """Get detailed product information with full cultural context"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get all attributes
        attributes = self.db.query(ProductAttribute).filter(
            ProductAttribute.product_id == product_id
        ).all()
        
        # Get all reviews with cultural context
        reviews = self.db.query(ProductReview).filter(
            ProductReview.product_id == product_id
        ).all()
        
        # Get cultural collections
        collections = self.db.query(CulturalCollection).join(
            ProductCollection, CulturalCollection.id == ProductCollection.collection_id
        ).filter(ProductCollection.product_id == product_id).all()
        
        # Calculate ratings breakdown
        rating_counts = {i: 0 for i in range(1, 6)}
        for review in reviews:
            rating_counts[review.rating] += 1
        
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        return {
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "currency": product.currency,
                "category": product.category,
                "image_url": product.image_url,
                "stock": product.stock,
                "created_at": product.created_at.isoformat()
            },
            "cultural_attributes": {
                "ceremonial": [attr for attr in attributes if attr.attribute_type == "ceremonial"],
                "cultural": [attr for attr in attributes if attr.attribute_type == "cultural"],
                "functional": [attr for attr in attributes if attr.attribute_type == "functional"]
            },
            "reviews": {
                "average_rating": round(avg_rating, 1),
                "total_reviews": len(reviews),
                "rating_breakdown": rating_counts,
                "recent_reviews": [{
                    "id": rev.id,
                    "rating": rev.rating,
                    "review_text": rev.review_text,
                    "cultural_context": rev.cultural_context,
                    "ceremonial_seal": rev.ceremonial_seal,
                    "created_at": rev.created_at.isoformat(),
                    "is_verified": rev.is_verified
                } for rev in sorted(reviews, key=lambda x: x.created_at, reverse=True)[:10]]
            },
            "cultural_collections": [{
                "id": coll.id,
                "name": coll.name,
                "description": coll.description,
                "diaspora_region": coll.diaspora_region,
                "sigil": coll.sigil
            } for coll in collections],
            "message": "Product with complete cultural context"
        }
    
    def get_collections_by_region(self, diaspora_region: str = None) -> Dict:
        """Get cultural collections for specific diaspora regions"""
        query = self.db.query(CulturalCollection)
        
        if diaspora_region:
            query = query.filter(CulturalCollection.diaspora_region == diaspora_region)
        
        collections = query.all()
        
        enhanced_collections = []
        for collection in collections:
            # Get products in this collection
            product_count = self.db.query(ProductCollection).filter(
                ProductCollection.collection_id == collection.id
            ).count()
            
            enhanced_collections.append({
                "id": collection.id,
                "name": collection.name,
                "description": collection.description,
                "diaspora_region": collection.diaspora_region,
                "product_count": product_count,
                "sigil": collection.sigil,
                "is_featured": collection.is_featured,
                "created_at": collection.created_at.isoformat()
            })
        
        return {
            "total_collections": len(enhanced_collections),
            "collections": enhanced_collections,
            "region_filter": diaspora_region,
            "message": "Cultural collections with diaspora context"
        }

def get_diaspora_catalog_service(db: Session = None) -> DiasporaProductCatalog:
    """Get diaspora catalog service instance"""
    if db is None:
        db = SessionLocal()
    return DiasporaProductCatalog(db)

# Utility functions for seeding data
def seed_sample_categories(db: Session):
    """Seed sample categories with cultural significance"""
    catalog_service = DiasporaProductCatalog(db)
    
    sample_categories = [
        {
            "name": "Sacred Artifacts",
            "description": "Ceremonial items with deep cultural significance",
            "cultural_significance": "Objects that carry the weight of ancestral wisdom and serve as bridges between past and present"
        },
        {
            "name": "Diaspora Literature",
            "description": "Books and writings that honor diaspora experiences",
            "cultural_significance": "Literary works that preserve cultural memory and provide guidance for dispersed communities"
        },
        {
            "name": "Sovereign Tools",
            "description": "Practical instruments for autonomous living",
            "cultural_significance": "Tools that enable self-sufficiency and independence within diaspora communities"
        },
        {
            "name": "Cultural Textiles",
            "description": "Fabrics and garments with traditional patterns",
            "cultural_significance": "Textiles that maintain cultural identity and serve as markers of heritage"
        }
    ]
    
    for category_data in sample_categories:
        try:
            catalog_service.create_category(
                name=category_data["name"],
                description=category_data["description"],
                cultural_significance=category_data["cultural_significance"],
                creator_role="custodian"
            )
            logger.info(f"Sample category created: {category_data['name']}")
        except HTTPException as e:
            if "already exists" in str(e.detail):
                logger.info(f"Category already exists: {category_data['name']}")
            else:
                logger.error(f"Error creating category {category_data['name']}: {e.detail}")
        except Exception as e:
            logger.error(f"Unexpected error creating category {category_data['name']}: {e}")

def seed_sample_collections(db: Session, curator_id: str):
    """Seed sample cultural collections"""
    catalog_service = DiasporaProductCatalog(db)
    
    sample_collections = [
        {
            "name": "African Diaspora Heritage",
            "description": "Products celebrating African diaspora culture and history",
            "diaspora_region": "African Diaspora",
            "metadata": {"focus": "heritage", "themes": ["liberation", "unity", "ancestral wisdom"]}
        },
        {
            "name": "Latin American Solidarity",
            "description": "Items that honor Latin American diaspora communities",
            "diaspora_region": "Latin American Diaspora",
            "metadata": {"focus": "solidarity", "themes": ["resistance", "community", "cultural pride"]}
        },
        {
            "name": "Asian Diaspora Wisdom",
            "description": "Products reflecting Asian diaspora experiences and philosophies",
            "diaspora_region": "Asian Diaspora",
            "metadata": {"focus": "wisdom", "themes": ["balance", "perseverance", "innovation"]}
        },
        {
            "name": "Global Nomads Collection",
            "description": "Items for digitally connected diaspora communities",
            "diaspora_region": "Digital Nomad",
            "metadata": {"focus": "connectivity", "themes": ["mobility", "technology", "adaptation"]}
        }
    ]
    
    for collection_data in sample_collections:
        try:
            result = catalog_service.create_cultural_collection(
                name=collection_data["name"],
                description=collection_data["description"],
                diaspora_region=collection_data["diaspora_region"],
                curator_id=curator_id,
                metadata=collection_data["metadata"]
            )
            logger.info(f"Sample collection created: {collection_data['name']} - {result['collection_id']}")
        except Exception as e:
            logger.error(f"Error creating collection {collection_data['name']}: {e}")

if __name__ == "__main__":
    # Test the enhanced catalog service
    from sovereign_main import engine, SessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Test with a session
    db = SessionLocal()
    
    try:
        # Seed sample data
        seed_sample_categories(db)
        
        # Create a test curator (you'll need to provide a real user ID in practice)
        test_curator_id = "USER-TEST-CURATOR"
        seed_sample_collections(db, test_curator_id)
        
        # Test the enhanced catalog
        catalog_service = DiasporaProductCatalog(db)
        result = catalog_service.get_enhanced_product_catalog()
        print("Enhanced catalog:", json.dumps(result, indent=2, default=str))
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        db.close()