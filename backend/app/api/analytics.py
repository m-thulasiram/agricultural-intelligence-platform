import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from ..schemas import (
    AnalyticsResponse,
    DashboardSummaryResponse,
    DashboardStats,
    FeatureImportanceResponse,
    ModelPerformanceResponse,
    ExplainPredictionRequest,
    ExplainPredictionResponse,
)
from ..services import MLPipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_ml_pipeline() -> MLPipeline:
    return MLPipeline()


@router.get("", response_model=AnalyticsResponse, summary="Get analytics data with trends")
async def get_analytics():
    try:
        logger.info("Analytics data requested")
        return AnalyticsResponse(
            total_predictions=1250,
            average_health_index=0.72,
            high_risk_regions=["Region A", "Region B", "Region C"],
            climate_trends={
                "temperature": {"increasing": True, "rate": 0.05},
                "rainfall": {"decreasing": True, "rate": -0.03},
                "drought_frequency": {"increasing": True, "rate": 0.02},
            },
            crop_distribution={"Rice": 40, "Wheat": 25, "Maize": 20, "Other": 15},
        )
    except Exception as e:
        logger.error("Analytics fetch failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Analytics service unavailable")


@router.get("/dashboard-summary", response_model=DashboardSummaryResponse, summary="Get dashboard summary data")
async def dashboard_summary():
    try:
        logger.info("Dashboard summary requested")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        import random
        random.seed(42)
        return DashboardSummaryResponse(
            stats=DashboardStats(totalPredictions=12847, activeRegions=24, avgHealthIndex=72.5, riskAlerts=8),
            healthOverview=[{"name": m, "health": round(50 + random.random() * 40, 1), "rainfall": round(20 + random.random() * 80, 1), "temperature": round(15 + random.random() * 20, 1)} for m in months],
            recentPredictions=[
                {"id": 1, "region": "North India", "crop": "Wheat", "healthIndex": 85, "risk": "Low", "date": "2025-03-15"},
                {"id": 2, "region": "South India", "crop": "Rice", "healthIndex": 62, "risk": "Moderate", "date": "2025-03-14"},
                {"id": 3, "region": "East India", "crop": "Sugarcane", "healthIndex": 45, "risk": "High", "date": "2025-03-14"},
                {"id": 4, "region": "West India", "crop": "Cotton", "healthIndex": 78, "risk": "Low", "date": "2025-03-13"},
                {"id": 5, "region": "Central India", "crop": "Maize", "healthIndex": 55, "risk": "Moderate", "date": "2025-03-13"},
            ],
            climateTrend=[
                {"year": "2020", "avg": 24.5, "min": 18.2, "max": 31.8},
                {"year": "2021", "avg": 25.1, "min": 19.0, "max": 32.5},
                {"year": "2022", "avg": 24.8, "min": 18.5, "max": 32.0},
                {"year": "2023", "avg": 25.6, "min": 19.3, "max": 33.1},
                {"year": "2024", "avg": 26.2, "min": 20.1, "max": 33.8},
            ],
            cropDistribution=[
                {"name": "Wheat", "value": 28},
                {"name": "Rice", "value": 24},
                {"name": "Maize", "value": 18},
                {"name": "Sugarcane", "value": 15},
                {"name": "Cotton", "value": 10},
                {"name": "Others", "value": 5},
            ],
            alerts=[
                {"type": "warning", "message": "Drought risk increasing in Central India", "time": "2h ago"},
                {"type": "info", "message": "Optimal planting window for Rabi crops approaching", "time": "5h ago"},
                {"type": "success", "message": "North India soil moisture levels are healthy", "time": "1d ago"},
                {"type": "error", "message": "Pest outbreak reported in East India rice fields", "time": "2d ago"},
            ],
        )
    except Exception as e:
        logger.error("Dashboard summary failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Dashboard service unavailable")


@router.get("/feature-importance", response_model=FeatureImportanceResponse, summary="Get ML model feature importance")
async def feature_importance(
    pipeline: MLPipeline = Depends(get_ml_pipeline),
):
    try:
        logger.info("Feature importance requested")
        features = pipeline.get_feature_importance()
        return FeatureImportanceResponse(features=features, model_name="XGBoost")
    except Exception as e:
        logger.error("Feature importance fetch failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Feature importance service unavailable")


@router.get("/model-performance", response_model=ModelPerformanceResponse, summary="Get model performance metrics")
async def model_performance(
    pipeline: MLPipeline = Depends(get_ml_pipeline),
):
    try:
        logger.info("Model performance requested")
        perf = pipeline.get_model_performance()
        return ModelPerformanceResponse(
            accuracy=perf.get("accuracy", 0.0),
            precision=perf.get("precision", 0.0),
            recall=perf.get("recall", 0.0),
            f1_score=perf.get("f1_score", 0.0),
            mae=perf.get("mae", 0.0),
            rmse=perf.get("rmse", 0.0),
            r2_score=perf.get("r2_score", 0.0),
            model_name=perf.get("model_name", "XGBoost"),
            training_date=perf.get("training_date", "2025-01-15"),
        )
    except Exception as e:
        logger.error("Model performance fetch failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Model performance service unavailable")


@router.post("/explain-prediction", response_model=ExplainPredictionResponse, summary="Explain a prediction with SHAP/LIME")
async def explain_prediction(
    request: ExplainPredictionRequest,
    pipeline: MLPipeline = Depends(get_ml_pipeline),
):
    try:
        logger.info(
            "Explain prediction request: model=%s",
            request.model_name,
        )
        explanation = pipeline.explain_prediction(
            features=request.features,
            model_name=request.model_name,
        )
        return ExplainPredictionResponse(
            explanation_method=explanation["explanation_method"],
            base_value=explanation["base_value"],
            prediction=explanation["prediction"],
            shap_values=explanation["shap_values"],
            top_features=explanation["top_features"],
        )
    except Exception as e:
        logger.error("Prediction explanation failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Explanation service unavailable")
