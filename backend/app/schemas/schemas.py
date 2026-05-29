from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150, description="Unique username")
    email: str = Field(..., max_length=255, description="User email address")
    password: str = Field(..., min_length=6, max_length=255, description="User password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        return v.lower().strip()


class UserLogin(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class TokenData(BaseModel):
    username: Optional[str] = None


class PredictRequest(BaseModel):
    Year: int = Field(..., ge=1950, le=2100, description="Year for prediction")
    avg_rainfall: float = Field(..., ge=0, description="Average rainfall in mm")
    pesticides: float = Field(..., ge=0, description="Pesticide usage in tonnes")
    avg_temp: float = Field(..., description="Average temperature in celsius")
    area: float = Field(..., ge=0, description="Area in hectares")
    item: str = Field(..., min_length=1, description="Crop item name")


class PredictResponse(BaseModel):
    predicted_yield: float = Field(..., description="Predicted crop yield")
    item: str
    year: int
    confidence: Optional[float] = None


class FutureForecastRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    forecast_years: str = Field("5", description="Forecast preset: 5, 10, 20, 50, or custom")
    custom_years: Optional[List[int]] = Field(None, description="Custom list of years if forecast_years is 'custom'")


class FutureForecastResponse(BaseModel):
    region: str
    forecasts: List[Dict[str, Any]] = Field(..., description="List of yearly forecast data")


class DiseaseRiskRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    crop_type: str = Field(..., min_length=1, description="Crop type")
    year: int = Field(..., ge=2024, le=2100, description="Target year")


class DiseaseRiskResponse(BaseModel):
    region: str
    crop_type: str
    year: int
    pest_attack_probability: float
    disease_outbreak_probability: float
    seasonal_risk: str
    preventive_measures: List[str]


class CropRecommendationRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    year: int = Field(..., ge=2024, le=2100, description="Target year")
    climate_data: Optional[Dict[str, Any]] = Field(None, description="Optional climate data override")


class CropRecommendationResponse(BaseModel):
    region: str
    year: int
    recommended_crops: List[Dict[str, Any]]
    fertilizer_plan: Dict[str, Any]
    irrigation_schedule: Dict[str, Any]
    water_saving_strategies: List[str]
    pest_prevention_methods: List[str]


class AnalyticsResponse(BaseModel):
    total_predictions: int
    average_health_index: float
    high_risk_regions: List[str]
    climate_trends: Dict[str, Any]
    crop_distribution: Dict[str, int]


class DashboardStats(BaseModel):
    totalPredictions: int
    activeRegions: int
    avgHealthIndex: float
    riskAlerts: int


class DashboardSummaryResponse(BaseModel):
    stats: DashboardStats
    healthOverview: List[Dict[str, Any]]
    recentPredictions: List[Dict[str, Any]]
    climateTrend: List[Dict[str, Any]]
    cropDistribution: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]


class ClimateForecastResponse(BaseModel):
    id: int
    region: str
    forecast_year: int
    rainfall_predicted: float
    temperature_predicted: float
    drought_probability: float
    flood_probability: float
    climate_impact_score: float
    model_used: str
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class CropHealthResponse(BaseModel):
    id: int
    region: str
    crop_type: str
    year: int
    health_index: float
    yield_forecast: float
    risk_score: float
    confidence_score: float
    health_category: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True


class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]
    total: int
    successful: int
    failed: int


class ModelComparisonRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    forecast_years: int = Field(5, ge=1, le=50, description="Number of years to forecast")


class ModelMetric(BaseModel):
    model_name: str
    mae: float
    rmse: float
    r2: float
    mape: Optional[float] = None


class ModelComparisonResponse(BaseModel):
    region: str
    models: List[ModelMetric]
    best_model: str
    forecasts: Dict[str, List[Dict[str, Any]]]


class FertilizerPlanRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    crop_type: str = Field(..., min_length=1, description="Crop type")
    year: int = Field(..., ge=2024, le=2100, description="Target year")
    soil_data: Optional[Dict[str, Any]] = Field(None, description="Optional soil data override")


class FertilizerPlanResponse(BaseModel):
    region: str
    crop_type: str
    year: int
    recommended_fertilizers: List[Dict[str, Any]]
    schedule: List[Dict[str, Any]]
    total_cost_estimate: Optional[float] = None


class IrrigationScheduleRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    crop_type: str = Field(..., min_length=1, description="Crop type")
    year: int = Field(..., ge=2024, le=2100, description="Target year")
    climate_data: Optional[Dict[str, Any]] = Field(None, description="Optional climate data override")


class IrrigationScheduleResponse(BaseModel):
    region: str
    crop_type: str
    year: int
    schedule: List[Dict[str, Any]]
    total_water_requirement: float
    water_saving_strategies: List[str]


class FeatureImportanceResponse(BaseModel):
    features: List[Dict[str, Any]]
    model_name: str


class ModelPerformanceResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mae: float
    rmse: float
    r2_score: float
    confusion_matrix: Optional[List[List[int]]] = None
    model_name: str
    training_date: str


class ExplainPredictionRequest(BaseModel):
    features: Dict[str, Any] = Field(..., description="Feature values for explanation")
    model_name: str = Field("xgboost", description="Model to explain")


class ExplainPredictionResponse(BaseModel):
    explanation_method: str
    base_value: float
    prediction: float
    shap_values: Dict[str, float]
    top_features: List[Dict[str, Any]]


class ReportRequest(BaseModel):
    report_type: str = Field(..., pattern="^(forecast|prediction|disease|analytics|full)$", description="Type of report")
    region: Optional[str] = Field(None, description="Region filter")
    year: Optional[int] = Field(None, description="Year filter")
    include_charts: bool = Field(True, description="Include visualizations")


class ReportResponse(BaseModel):
    report_id: str
    status: str
    message: str
    download_url: Optional[str] = None
    generated_at: datetime


class DynamicTimelineRequest(BaseModel):
    region: str = Field(..., min_length=1, description="Region name")
    start_year: int = Field(..., ge=1950, le=2100, description="Start year Y0")
    n: int = Field(..., ge=0, le=200, description="Number of years to forecast (total years = n+1)")


class DynamicTimelineEntry(BaseModel):
    year: int
    rainfall: float
    temperature: float
    humidity: float
    fertilizer_usage: float
    pesticide_usage: float
    crop_yield: float
    crop_health_index: float
    disease_risk: float
    pest_risk: float
    water_stress: float
    sustainability_score: float


class DynamicTimelineResponse(BaseModel):
    region: str
    start_year: int
    end_year: int
    total_years: int
    timeline: List[DynamicTimelineEntry]


class ForecastHistoryResponse(BaseModel):
    region: str
    history: List[ClimateForecastResponse]
    total: int


class DiseaseBatchResponse(BaseModel):
    results: List[DiseaseRiskResponse]
    total: int
    successful: int
    failed: int
