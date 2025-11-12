# app/models.py
from sqlalchemy import Column, String, JSON, Float
from app.db import Base

class WorkflowModel(Base):
    __tablename__ = "workflows"
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    phase = Column(String, index=True)
    data = Column(JSON)
    created_at = Column(Float)
    updated_at = Column(Float)