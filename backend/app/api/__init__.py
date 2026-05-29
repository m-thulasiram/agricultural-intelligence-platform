from fastapi import APIRouter

from .predictions import router as predictions_router
from .forecasts import router as forecasts_router
from .diseases import router as diseases_router
from .recommendations import router as recommendations_router
from .analytics import router as analytics_router
from .reports import router as reports_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(predictions_router, tags=["Predictions"])
api_router.include_router(forecasts_router, tags=["Forecasts"])
api_router.include_router(diseases_router, tags=["Diseases"])
api_router.include_router(recommendations_router, tags=["Recommendations"])
api_router.include_router(analytics_router, tags=["Analytics"])
api_router.include_router(reports_router, tags=["Reports"])

__all__ = ["api_router"]
