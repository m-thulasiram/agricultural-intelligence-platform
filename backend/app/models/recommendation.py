from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(150), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    recommended_crops = Column(JSON, nullable=False, comment="List of recommended crops with details")
    fertilizer_plan = Column(JSON, nullable=False, comment="Fertilizer schedule and recommendations")
    irrigation_schedule = Column(JSON, nullable=False, comment="Irrigation timing and amounts")
    water_saving_strategies = Column(JSON, nullable=False, comment="Water conservation methods")
    pest_prevention_methods = Column(JSON, nullable=False, comment="Pest control recommendations")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
