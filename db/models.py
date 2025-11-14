# db/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contributor(Base):
    __tablename__ = "contributors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    roles = Column(JSON, nullable=False)
    seal = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Scroll(Base):
    __tablename__ = "scrolls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    contributor_id = Column(Integer, ForeignKey("contributors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    contributor = relationship("Contributor")

class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReplayArchive(Base):
    __tablename__ = "replay_archives"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(100), nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)