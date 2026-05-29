import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query

from ..schemas import (
    FutureForecastRequest,
    FutureForecastResponse,
    ModelComparisonRequest,
    ModelComparisonResponse,
    ForecastHistoryResponse,
    ClimateForecastResponse,
    DynamicTimelineRequest,
    DynamicTimelineResponse,
)
from ..services import ClimateForecaster
from ..utils.helpers import parse_forecast_years

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/forecast", tags=["Forecasts"])


def get_climate_forecaster() -> ClimateForecaster:
    return ClimateForecaster()


@router.post("/future", response_model=FutureForecastResponse, summary="Get future climate forecast")
async def future_forecast(
    request: FutureForecastRequest,
    forecaster: ClimateForecaster = Depends(get_climate_forecaster),
):
    try:
        years = parse_forecast_years(request.forecast_years, request.custom_years)
        logger.info(
            "Future forecast request: region=%s, years=%s",
            request.region, years,
        )
        forecasts = forecaster.forecast_future(region=request.region, years=years)
        return FutureForecastResponse(region=request.region, forecasts=forecasts)
    except ValueError as e:
        logger.warning("Validation error in forecast: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Forecast failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Forecast service unavailable")


@router.post("/compare-models", response_model=ModelComparisonResponse, summary="Compare forecasting models")
async def compare_models(
    request: ModelComparisonRequest,
    forecaster: ClimateForecaster = Depends(get_climate_forecaster),
):
    try:
        logger.info(
            "Model comparison request: region=%s, years=%d",
            request.region, request.forecast_years,
        )
        result = forecaster.compare_models(
            region=request.region,
            forecast_years=request.forecast_years,
        )
        return ModelComparisonResponse(**result)
    except Exception as e:
        logger.error("Model comparison failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Model comparison service unavailable")


@router.post("/timeline", response_model=DynamicTimelineResponse, summary="Generate dynamic yearly timeline")
async def dynamic_timeline(
    request: DynamicTimelineRequest,
    forecaster: ClimateForecaster = Depends(get_climate_forecaster),
):
    try:
        logger.info(
            "Dynamic timeline request: region=%s, start_year=%d, n=%d",
            request.region, request.start_year, request.n,
        )
        result = forecaster.generate_dynamic_timeline(
            region=request.region,
            start_year=request.start_year,
            n=request.n,
        )
        return DynamicTimelineResponse(
            region=result["region"],
            start_year=result["start_year"],
            end_year=result["end_year"],
            total_years=result["total_years"],
            timeline=result["timeline"],
        )
    except Exception as e:
        logger.error("Dynamic timeline failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Timeline generation failed")


@router.get("/history/{region}", response_model=ForecastHistoryResponse, summary="Get historical forecasts for a region")
async def forecast_history(
    region: str,
    limit: int = Query(100, ge=1, le=1000),
    forecaster: ClimateForecaster = Depends(get_climate_forecaster),
):
    try:
        logger.info("Forecast history request: region=%s, limit=%d", region, limit)
        history = forecaster.get_forecast_history(region=region, limit=limit)
        items = []
        for h in history:
            items.append(
                ClimateForecastResponse(
                    id=h["id"],
                    region=h["region"],
                    forecast_year=h["forecast_year"],
                    rainfall_predicted=h["rainfall_predicted"],
                    temperature_predicted=h["temperature_predicted"],
                    drought_probability=h["drought_probability"],
                    flood_probability=h["flood_probability"],
                    climate_impact_score=h["climate_impact_score"],
                    model_used=h["model_used"],
                    confidence_score=h["confidence_score"],
                    created_at=h["created_at"],
                )
            )
        return ForecastHistoryResponse(region=region, history=items, total=len(items))
    except Exception as e:
        logger.error("Forecast history fetch failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch forecast history")
