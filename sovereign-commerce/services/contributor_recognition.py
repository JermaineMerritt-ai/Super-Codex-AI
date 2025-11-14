#!/usr/bin/env python3
"""
Contributor Recognition System for Diaspora Community
Honoring community members and contributors with ceremonial recognition

Built with dignity to celebrate diaspora community contributions.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from decimal import Decimal
import json
import secrets
from collections import defaultdict
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, DECIMAL, Integer, Text, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

from sovereign_main import Base, User, SessionLocal
from funder_dashboard import FunderActivity, FunderMilestone

# Logging setup
logger = logging.getLogger(__name__)

# Recognition System Models
class ContributionCategory(str, Enum):
    """Categories of community contributions"""
    FINANCIAL = "financial_support"
    CULTURAL = "cultural_preservation"
    EDUCATIONAL = "educational_advancement"
    COMMUNITY = "community_building"
    MENTORSHIP = "mentorship_guidance"
    ADVOCACY = "advocacy_leadership"
    INNOVATION = "innovation_development"
    STEWARDSHIP = "environmental_stewardship"

class RecognitionLevel(str, Enum):
    """Levels of recognition within the community"""
    EMERGING = "emerging_contributor"
    ESTABLISHED = "established_contributor"
    DISTINGUISHED = "distinguished_contributor"
    LEGENDARY = "legendary_contributor"
    ANCESTRAL = "ancestral_honor"

class ContributorProfile(Base):
    __tablename__ = "contributor_profiles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), unique=True)
    display_name = Column(String)
    bio_statement = Column(Text)
    cultural_heritage = Column(Text)  # JSON cultural background
    expertise_areas = Column(Text)  # JSON areas of expertise
    contribution_categories = Column(Text)  # JSON active contribution categories
    recognition_level = Column(String)  # Current recognition level
    honor_points = Column(Integer, default=0)  # Accumulated honor points
    visibility_setting = Column(String, default="community")  # public, community, private
    profile_sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ContributionRecord(Base):
    __tablename__ = "contribution_records"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    contributor_id = Column(String, ForeignKey('contributor_profiles.id'))
    contribution_category = Column(String)
    contribution_type = Column(String)  # Specific type within category
    contribution_title = Column(String)
    contribution_description = Column(Text)
    cultural_impact = Column(Text)  # Cultural significance of contribution
    beneficiary_community = Column(String)  # Which diaspora community benefits
    honor_points_awarded = Column(Integer, default=0)
    verification_status = Column(String, default="pending")  # pending, verified, featured
    verified_by = Column(String, ForeignKey('users.id'))
    verified_at = Column(DateTime)
    contribution_evidence = Column(Text)  # JSON evidence/documentation
    ceremonial_seal = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class CommunityHonor(Base):
    __tablename__ = "community_honors"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    honor_title = Column(String, unique=True)
    honor_description = Column(Text)
    cultural_significance = Column(Text)  # Cultural meaning of this honor
    required_categories = Column(Text)  # JSON categories required for this honor
    minimum_honor_points = Column(Integer)
    minimum_recognition_level = Column(String)
    honor_ceremony = Column(Text)  # JSON ceremony details
    honor_sigil = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class HonorAwarded(Base):
    __tablename__ = "honors_awarded"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    honor_id = Column(String, ForeignKey('community_honors.id'))
    contributor_id = Column(String, ForeignKey('contributor_profiles.id'))
    awarded_by = Column(String, ForeignKey('users.id'))
    ceremony_details = Column(Text)  # JSON ceremony performed
    community_witnesses = Column(Text)  # JSON community members who witnessed
    cultural_blessing = Column(Text)  # Special blessing or dedication
    honor_certificate = Column(String)  # Unique certificate identifier
    awarded_at = Column(DateTime, default=datetime.utcnow)
    is_featured = Column(Boolean, default=False)

class ContributorEndorsement(Base):
    __tablename__ = "contributor_endorsements"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    contributor_id = Column(String, ForeignKey('contributor_profiles.id'))
    endorser_id = Column(String, ForeignKey('contributor_profiles.id'))
    endorsement_category = Column(String)
    endorsement_text = Column(Text)
    cultural_context = Column(Text)  # Cultural context of endorsement
    strength_rating = Column(Integer)  # 1-10 strength of endorsement
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CommunityRecognitionEvent(Base):
    __tablename__ = "recognition_events"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True)
    event_title = Column(String)
    event_description = Column(Text)
    event_type = Column(String)  # ceremony, celebration, memorial, gathering
    cultural_elements = Column(Text)  # JSON cultural ceremony elements
    honored_contributors = Column(Text)  # JSON list of contributors being honored
    community_participants = Column(Text)  # JSON participants in the event
    event_ceremony = Column(Text)  # JSON ceremonial procedures
    event_date = Column(DateTime)
    organizer_id = Column(String, ForeignKey('users.id'))
    event_sigil = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Contributor Recognition Service
class ContributorRecognitionService:
    """Service for managing contributor recognition and honors"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
    
    def create_contributor_profile(self, user_id: str, display_name: str, bio_statement: str,
                                 cultural_heritage: Dict, expertise_areas: List[str],
                                 contribution_categories: List[str] = None) -> Dict:
        """Create a contributor profile"""
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if profile already exists
        existing_profile = self.db.query(ContributorProfile).filter(
            ContributorProfile.user_id == user_id
        ).first()
        if existing_profile:
            raise HTTPException(status_code=409, detail="Contributor profile already exists")
        
        profile_id = f"CONTRIB-{secrets.token_hex(6).upper()}"
        profile_sigil = f"SIGIL-CONTRIB-{secrets.token_hex(4).upper()}"
        
        contributor_profile = ContributorProfile(
            id=profile_id,
            user_id=user_id,
            display_name=display_name,
            bio_statement=bio_statement,
            cultural_heritage=json.dumps(cultural_heritage),
            expertise_areas=json.dumps(expertise_areas),
            contribution_categories=json.dumps(contribution_categories or []),
            recognition_level=RecognitionLevel.EMERGING.value,
            profile_sigil=profile_sigil
        )
        
        self.db.add(contributor_profile)
        self.db.commit()
        self.db.refresh(contributor_profile)
        
        self.logger.info(f"Contributor profile created: {display_name} with sigil {profile_sigil}")
        
        return {
            "profile_id": profile_id,
            "display_name": display_name,
            "recognition_level": RecognitionLevel.EMERGING.value,
            "profile_sigil": profile_sigil,
            "message": "Contributor profile created with community recognition"
        }
    
    def record_contribution(self, contributor_id: str, contribution_category: str,
                          contribution_type: str, contribution_title: str,
                          contribution_description: str, cultural_impact: str,
                          beneficiary_community: str, contribution_evidence: Dict = None) -> Dict:
        """Record a new contribution"""
        # Verify contributor profile exists
        contributor = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == contributor_id
        ).first()
        if not contributor:
            raise HTTPException(status_code=404, detail="Contributor profile not found")
        
        record_id = f"RECORD-{secrets.token_hex(6).upper()}"
        ceremonial_seal = f"SEAL-CONTRIB-{secrets.token_hex(4).upper()}"
        
        # Calculate honor points based on contribution category and impact
        honor_points = self._calculate_contribution_honor_points(
            contribution_category, contribution_type, cultural_impact
        )
        
        contribution_record = ContributionRecord(
            id=record_id,
            contributor_id=contributor_id,
            contribution_category=contribution_category,
            contribution_type=contribution_type,
            contribution_title=contribution_title,
            contribution_description=contribution_description,
            cultural_impact=cultural_impact,
            beneficiary_community=beneficiary_community,
            honor_points_awarded=honor_points,
            contribution_evidence=json.dumps(contribution_evidence) if contribution_evidence else None,
            ceremonial_seal=ceremonial_seal
        )
        
        self.db.add(contribution_record)
        
        # Update contributor's honor points and check for level advancement
        contributor.honor_points += honor_points
        self._check_recognition_level_advancement(contributor)
        
        self.db.commit()
        
        self.logger.info(f"Contribution recorded: {contribution_title} for {contributor.display_name}")
        
        return {
            "record_id": record_id,
            "contribution_title": contribution_title,
            "honor_points_awarded": honor_points,
            "total_honor_points": contributor.honor_points,
            "recognition_level": contributor.recognition_level,
            "ceremonial_seal": ceremonial_seal,
            "message": "Contribution recorded with ceremonial honors"
        }
    
    def verify_contribution(self, record_id: str, verifier_id: str, verification_notes: str = None) -> Dict:
        """Verify a contribution record (flamekeeper/custodian only)"""
        # Verify verifier has appropriate role
        verifier = self.db.query(User).filter(User.id == verifier_id).first()
        if not verifier or verifier.role not in ["flamekeeper", "custodian"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges for verification")
        
        # Get contribution record
        record = self.db.query(ContributionRecord).filter(
            ContributionRecord.id == record_id
        ).first()
        if not record:
            raise HTTPException(status_code=404, detail="Contribution record not found")
        
        if record.verification_status == "verified":
            raise HTTPException(status_code=409, detail="Contribution already verified")
        
        # Verify the contribution
        record.verification_status = "verified"
        record.verified_by = verifier_id
        record.verified_at = datetime.utcnow()
        
        # Award bonus honor points for verified contributions
        bonus_points = int(record.honor_points_awarded * 0.5)  # 50% bonus
        
        contributor = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == record.contributor_id
        ).first()
        
        contributor.honor_points += bonus_points
        self._check_recognition_level_advancement(contributor)
        
        self.db.commit()
        
        self.logger.info(f"Contribution verified: {record.contribution_title} by {verifier.sigil}")
        
        return {
            "record_id": record_id,
            "verification_status": "verified",
            "bonus_points_awarded": bonus_points,
            "verified_by": verifier.sigil,
            "verified_at": record.verified_at.isoformat(),
            "message": "Contribution verified with ceremonial approval"
        }
    
    def create_community_honor(self, honor_title: str, honor_description: str,
                             cultural_significance: str, required_categories: List[str],
                             minimum_honor_points: int, minimum_recognition_level: str,
                             honor_ceremony: Dict, creator_role: str) -> Dict:
        """Create a new community honor"""
        if creator_role not in ["flamekeeper", "custodian"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges for honor creation")
        
        # Check if honor already exists
        existing_honor = self.db.query(CommunityHonor).filter(
            CommunityHonor.honor_title == honor_title
        ).first()
        if existing_honor:
            raise HTTPException(status_code=409, detail="Honor title already exists")
        
        honor_id = f"HONOR-{secrets.token_hex(6).upper()}"
        honor_sigil = f"SIGIL-HONOR-{secrets.token_hex(4).upper()}"
        
        community_honor = CommunityHonor(
            id=honor_id,
            honor_title=honor_title,
            honor_description=honor_description,
            cultural_significance=cultural_significance,
            required_categories=json.dumps(required_categories),
            minimum_honor_points=minimum_honor_points,
            minimum_recognition_level=minimum_recognition_level,
            honor_ceremony=json.dumps(honor_ceremony),
            honor_sigil=honor_sigil
        )
        
        self.db.add(community_honor)
        self.db.commit()
        self.db.refresh(community_honor)
        
        self.logger.info(f"Community honor created: {honor_title} with sigil {honor_sigil}")
        
        return {
            "honor_id": honor_id,
            "honor_title": honor_title,
            "minimum_honor_points": minimum_honor_points,
            "honor_sigil": honor_sigil,
            "message": "Community honor created with ceremonial dignity"
        }
    
    def award_honor(self, honor_id: str, contributor_id: str, awarded_by: str,
                   ceremony_details: Dict, community_witnesses: List[str] = None,
                   cultural_blessing: str = None) -> Dict:
        """Award a community honor to a contributor"""
        # Verify awarder has appropriate role
        awarder = self.db.query(User).filter(User.id == awarded_by).first()
        if not awarder or awarder.role not in ["flamekeeper", "custodian"]:
            raise HTTPException(status_code=403, detail="Insufficient privileges for honor awarding")
        
        # Verify honor exists
        honor = self.db.query(CommunityHonor).filter(CommunityHonor.id == honor_id).first()
        if not honor:
            raise HTTPException(status_code=404, detail="Honor not found")
        
        # Verify contributor exists and meets requirements
        contributor = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == contributor_id
        ).first()
        if not contributor:
            raise HTTPException(status_code=404, detail="Contributor not found")
        
        # Check if contributor meets honor requirements
        if contributor.honor_points < honor.minimum_honor_points:
            raise HTTPException(
                status_code=400, 
                detail=f"Contributor needs {honor.minimum_honor_points} honor points (has {contributor.honor_points})"
            )
        
        # Check recognition level requirement
        level_order = [level.value for level in RecognitionLevel]
        required_level_index = level_order.index(honor.minimum_recognition_level)
        current_level_index = level_order.index(contributor.recognition_level)
        
        if current_level_index < required_level_index:
            raise HTTPException(
                status_code=400,
                detail=f"Contributor needs {honor.minimum_recognition_level} level (has {contributor.recognition_level})"
            )
        
        # Check if honor already awarded
        existing_award = self.db.query(HonorAwarded).filter(
            HonorAwarded.honor_id == honor_id,
            HonorAwarded.contributor_id == contributor_id
        ).first()
        if existing_award:
            raise HTTPException(status_code=409, detail="Honor already awarded to this contributor")
        
        award_id = f"AWARD-{secrets.token_hex(6).upper()}"
        honor_certificate = f"CERT-{secrets.token_hex(8).upper()}"
        
        honor_awarded = HonorAwarded(
            id=award_id,
            honor_id=honor_id,
            contributor_id=contributor_id,
            awarded_by=awarded_by,
            ceremony_details=json.dumps(ceremony_details),
            community_witnesses=json.dumps(community_witnesses or []),
            cultural_blessing=cultural_blessing,
            honor_certificate=honor_certificate
        )
        
        self.db.add(honor_awarded)
        self.db.commit()
        
        self.logger.info(f"Honor awarded: {honor.honor_title} to {contributor.display_name}")
        
        return {
            "award_id": award_id,
            "honor_title": honor.honor_title,
            "contributor_name": contributor.display_name,
            "honor_certificate": honor_certificate,
            "awarded_by": awarder.sigil,
            "ceremony_performed": True,
            "message": "Honor awarded with ceremonial dignity and community recognition"
        }
    
    def create_endorsement(self, contributor_id: str, endorser_id: str, endorsement_category: str,
                         endorsement_text: str, cultural_context: str, strength_rating: int) -> Dict:
        """Create an endorsement between contributors"""
        # Verify both contributor profiles exist
        contributor = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == contributor_id
        ).first()
        if not contributor:
            raise HTTPException(status_code=404, detail="Contributor not found")
        
        endorser = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == endorser_id
        ).first()
        if not endorser:
            raise HTTPException(status_code=404, detail="Endorser profile not found")
        
        if contributor_id == endorser_id:
            raise HTTPException(status_code=400, detail="Cannot endorse yourself")
        
        if strength_rating < 1 or strength_rating > 10:
            raise HTTPException(status_code=400, detail="Strength rating must be between 1 and 10")
        
        endorsement_id = f"ENDORSE-{secrets.token_hex(6).upper()}"
        
        endorsement = ContributorEndorsement(
            id=endorsement_id,
            contributor_id=contributor_id,
            endorser_id=endorser_id,
            endorsement_category=endorsement_category,
            endorsement_text=endorsement_text,
            cultural_context=cultural_context,
            strength_rating=strength_rating
        )
        
        self.db.add(endorsement)
        self.db.commit()
        
        self.logger.info(f"Endorsement created: {endorser.display_name} endorsed {contributor.display_name}")
        
        return {
            "endorsement_id": endorsement_id,
            "endorser_name": endorser.display_name,
            "contributor_name": contributor.display_name,
            "endorsement_category": endorsement_category,
            "strength_rating": strength_rating,
            "message": "Endorsement created with community recognition"
        }
    
    def get_contributor_recognition_profile(self, contributor_id: str) -> Dict:
        """Get comprehensive contributor recognition profile"""
        contributor = self.db.query(ContributorProfile).filter(
            ContributorProfile.id == contributor_id
        ).first()
        if not contributor:
            raise HTTPException(status_code=404, detail="Contributor not found")
        
        # Get contribution records
        contributions = self.db.query(ContributionRecord).filter(
            ContributionRecord.contributor_id == contributor_id
        ).order_by(ContributionRecord.created_at.desc()).all()
        
        # Get honors awarded
        honors = self.db.query(HonorAwarded).join(
            CommunityHonor, HonorAwarded.honor_id == CommunityHonor.id
        ).filter(HonorAwarded.contributor_id == contributor_id).all()
        
        # Get endorsements received
        endorsements = self.db.query(ContributorEndorsement).filter(
            ContributorEndorsement.contributor_id == contributor_id
        ).all()
        
        # Calculate contribution statistics
        verified_contributions = [c for c in contributions if c.verification_status == "verified"]
        total_honor_points = sum(c.honor_points_awarded for c in verified_contributions)
        
        # Get contribution breakdown by category
        contribution_by_category = defaultdict(int)
        for contrib in verified_contributions:
            contribution_by_category[contrib.contribution_category] += 1
        
        return {
            "contributor": {
                "id": contributor.id,
                "display_name": contributor.display_name,
                "bio_statement": contributor.bio_statement,
                "cultural_heritage": json.loads(contributor.cultural_heritage),
                "expertise_areas": json.loads(contributor.expertise_areas),
                "recognition_level": contributor.recognition_level,
                "honor_points": contributor.honor_points,
                "profile_sigil": contributor.profile_sigil,
                "member_since": contributor.created_at.isoformat()
            },
            "contribution_summary": {
                "total_contributions": len(contributions),
                "verified_contributions": len(verified_contributions),
                "total_honor_points": total_honor_points,
                "contributions_by_category": dict(contribution_by_category),
                "recent_contributions": [{
                    "title": c.contribution_title,
                    "category": c.contribution_category,
                    "type": c.contribution_type,
                    "cultural_impact": c.cultural_impact,
                    "honor_points": c.honor_points_awarded,
                    "verification_status": c.verification_status,
                    "created_at": c.created_at.isoformat()
                } for c in contributions[:10]]
            },
            "honors": [{
                "honor_title": honor.honor.honor_title if hasattr(honor, 'honor') else "Honor",
                "honor_certificate": honor.honor_certificate,
                "cultural_blessing": honor.cultural_blessing,
                "awarded_at": honor.awarded_at.isoformat()
            } for honor in honors],
            "endorsements": [{
                "endorser_id": end.endorser_id,
                "endorsement_category": end.endorsement_category,
                "endorsement_text": end.endorsement_text,
                "cultural_context": end.cultural_context,
                "strength_rating": end.strength_rating,
                "created_at": end.created_at.isoformat()
            } for end in endorsements],
            "message": "Complete contributor recognition profile with community honors"
        }
    
    def get_community_leaderboard(self, category_filter: str = None, 
                                region_filter: str = None, limit: int = 50) -> Dict:
        """Get community leaderboard of top contributors"""
        query = self.db.query(ContributorProfile).filter(
            ContributorProfile.visibility_setting.in_(["public", "community"])
        )
        
        # Apply filters if specified
        if region_filter:
            # Filter by cultural heritage region
            query = query.filter(ContributorProfile.cultural_heritage.contains(region_filter))
        
        # Order by honor points and limit
        top_contributors = query.order_by(
            ContributorProfile.honor_points.desc()
        ).limit(limit).all()
        
        leaderboard = []
        for rank, contributor in enumerate(top_contributors, 1):
            # Get recent contributions count
            recent_contributions = self.db.query(ContributionRecord).filter(
                ContributionRecord.contributor_id == contributor.id,
                ContributionRecord.verification_status == "verified",
                ContributionRecord.created_at >= datetime.utcnow() - timedelta(days=90)
            ).count()
            
            # Filter by category if specified
            if category_filter:
                category_contributions = self.db.query(ContributionRecord).filter(
                    ContributionRecord.contributor_id == contributor.id,
                    ContributionRecord.contribution_category == category_filter,
                    ContributionRecord.verification_status == "verified"
                ).count()
                
                if category_contributions == 0:
                    continue
            
            contributor_data = {
                "rank": rank,
                "display_name": contributor.display_name,
                "recognition_level": contributor.recognition_level,
                "honor_points": contributor.honor_points,
                "recent_contributions": recent_contributions,
                "profile_sigil": contributor.profile_sigil,
                "cultural_heritage": json.loads(contributor.cultural_heritage) if contributor.cultural_heritage else {}
            }
            
            leaderboard.append(contributor_data)
        
        return {
            "total_contributors": len(leaderboard),
            "category_filter": category_filter,
            "region_filter": region_filter,
            "leaderboard": leaderboard,
            "recognition_levels": [level.value for level in RecognitionLevel],
            "contribution_categories": [cat.value for cat in ContributionCategory],
            "message": "Community leaderboard celebrating diaspora contributors"
        }
    
    def _calculate_contribution_honor_points(self, category: str, contribution_type: str, 
                                           cultural_impact: str) -> int:
        """Calculate honor points for a contribution"""
        base_points = {
            ContributionCategory.FINANCIAL.value: 20,
            ContributionCategory.CULTURAL.value: 25,
            ContributionCategory.EDUCATIONAL.value: 30,
            ContributionCategory.COMMUNITY.value: 25,
            ContributionCategory.MENTORSHIP.value: 35,
            ContributionCategory.ADVOCACY.value: 30,
            ContributionCategory.INNOVATION.value: 40,
            ContributionCategory.STEWARDSHIP.value: 25
        }
        
        points = base_points.get(category, 15)
        
        # Bonus for high cultural impact
        if cultural_impact and len(cultural_impact) > 100:  # Detailed impact description
            points += 10
        
        return points
    
    def _check_recognition_level_advancement(self, contributor: ContributorProfile):
        """Check and update contributor recognition level based on honor points"""
        current_points = contributor.honor_points
        
        # Define level thresholds
        level_thresholds = {
            RecognitionLevel.EMERGING.value: 0,
            RecognitionLevel.ESTABLISHED.value: 500,
            RecognitionLevel.DISTINGUISHED.value: 2000,
            RecognitionLevel.LEGENDARY.value: 5000,
            RecognitionLevel.ANCESTRAL.value: 10000
        }
        
        # Find highest level contributor qualifies for
        new_level = RecognitionLevel.EMERGING.value
        for level, threshold in level_thresholds.items():
            if current_points >= threshold:
                new_level = level
        
        if new_level != contributor.recognition_level:
            old_level = contributor.recognition_level
            contributor.recognition_level = new_level
            contributor.updated_at = datetime.utcnow()
            
            self.logger.info(
                f"Recognition level advancement: {contributor.display_name} "
                f"advanced from {old_level} to {new_level}"
            )

def get_recognition_service(db: Session = None) -> ContributorRecognitionService:
    """Get contributor recognition service instance"""
    if db is None:
        db = SessionLocal()
    return ContributorRecognitionService(db)

# Utility functions for seeding data
def seed_community_honors(db: Session):
    """Seed sample community honors"""
    recognition_service = ContributorRecognitionService(db)
    
    sample_honors = [
        {
            "honor_title": "Cultural Preservation Guardian",
            "honor_description": "Dedicated to preserving and sharing diaspora cultural heritage",
            "cultural_significance": "Recognizes those who keep cultural traditions alive across generations",
            "required_categories": ["cultural_preservation", "educational_advancement"],
            "minimum_honor_points": 1000,
            "minimum_recognition_level": "established_contributor",
            "honor_ceremony": {
                "type": "blessing_ceremony",
                "elements": ["ancestral_acknowledgment", "cultural_blessing", "community_witness"],
                "duration": "ceremonial_hour"
            }
        },
        {
            "honor_title": "Community Bridge Builder",
            "honor_description": "Excellence in connecting and strengthening diaspora communities",
            "cultural_significance": "Honors those who build bridges between communities and generations",
            "required_categories": ["community_building", "mentorship_guidance"],
            "minimum_honor_points": 1500,
            "minimum_recognition_level": "established_contributor",
            "honor_ceremony": {
                "type": "unity_celebration",
                "elements": ["community_gathering", "shared_stories", "collective_blessing"],
                "duration": "community_day"
            }
        },
        {
            "honor_title": "Wisdom Keeper",
            "honor_description": "Master teacher and guide for diaspora community members",
            "cultural_significance": "Celebrates those who share knowledge and guide others on their journey",
            "required_categories": ["mentorship_guidance", "educational_advancement", "cultural_preservation"],
            "minimum_honor_points": 3000,
            "minimum_recognition_level": "distinguished_contributor",
            "honor_ceremony": {
                "type": "wisdom_recognition",
                "elements": ["elder_blessing", "knowledge_sharing", "successor_acknowledgment"],
                "duration": "sacred_gathering"
            }
        },
        {
            "honor_title": "Ancestral Honor",
            "honor_description": "Lifetime achievement in service to diaspora communities",
            "cultural_significance": "The highest honor recognizing extraordinary lifetime contributions to the diaspora",
            "required_categories": ["all_categories"],
            "minimum_honor_points": 8000,
            "minimum_recognition_level": "legendary_contributor",
            "honor_ceremony": {
                "type": "ancestral_ceremony",
                "elements": ["lifetime_celebration", "community_testimony", "eternal_recognition"],
                "duration": "ceremonial_week"
            }
        }
    ]
    
    for honor_data in sample_honors:
        try:
            recognition_service.create_community_honor(
                honor_title=honor_data["honor_title"],
                honor_description=honor_data["honor_description"],
                cultural_significance=honor_data["cultural_significance"],
                required_categories=honor_data["required_categories"],
                minimum_honor_points=honor_data["minimum_honor_points"],
                minimum_recognition_level=honor_data["minimum_recognition_level"],
                honor_ceremony=honor_data["honor_ceremony"],
                creator_role="custodian"
            )
            logger.info(f"Community honor created: {honor_data['honor_title']}")
        except HTTPException as e:
            if "already exists" in str(e.detail):
                logger.info(f"Honor already exists: {honor_data['honor_title']}")
            else:
                logger.error(f"Error creating honor {honor_data['honor_title']}: {e.detail}")
        except Exception as e:
            logger.error(f"Unexpected error creating honor {honor_data['honor_title']}: {e}")

if __name__ == "__main__":
    # Test the recognition service
    from sovereign_main import engine, SessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Test with a session
    db = SessionLocal()
    
    try:
        # Seed sample honors
        seed_community_honors(db)
        
        recognition_service = ContributorRecognitionService(db)
        
        # Test structure
        print("Recognition service initialized successfully")
        print("Recognition levels:", [level.value for level in RecognitionLevel])
        print("Contribution categories:", [cat.value for cat in ContributionCategory])
        
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        db.close()