from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class ClimateForecast(Base):
    __tablename__ = "climate_forecasts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(150), nullable=False, index=True)
    forecast_year = Column(Integer, nullable=False, index=True)
    rainfall_predicted = Column(Float, nullable=False)
    temperature_predicted = Column(Float, nullable=False)
    drought_probability = Column(Float, nullable=False)
    flood_probability = Column(Float, nullable=False)
    climate_impact_score = Column(Float, nullable=False)
    model_used = Column(String(150), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CropHealthPrediction(Base):
    __tablename__ = "crop_health_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(150), nullable=False, index=True)
    crop_type = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    health_index = Column(Float, nullable=False)
    yield_forecast = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    health_category = Column(String(50), nullable=False)
    model_used = Column(String(150), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DiseasePrediction(Base):
    __tablename__ = "disease_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(150), nullable=False, index=True)
    crop_type = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    pest_attack_probability = Column(Float, nullable=False)
    disease_outbreak_probability = Column(Float, nullable=False)
    seasonal_risk = Column(String(50), nullable=False)
    preventive_measures = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
