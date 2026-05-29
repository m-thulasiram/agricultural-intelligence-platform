from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    type = Column(String(100), nullable=False)
    region = Column(String(150), nullable=False, index=True)
    soil_type = Column(String(100), nullable=False)
    water_requirement = Column(Float, nullable=False, comment="Water requirement in mm per season")
    temperature_min = Column(Float, nullable=False)
    temperature_max = Column(Float, nullable=False)
    growing_season = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
