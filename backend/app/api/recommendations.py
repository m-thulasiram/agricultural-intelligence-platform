import logging

from fastapi import APIRouter, HTTPException, Depends

from ..schemas import (
    CropRecommendationRequest,
    CropRecommendationResponse,
    FertilizerPlanRequest,
    FertilizerPlanResponse,
    IrrigationScheduleRequest,
    IrrigationScheduleResponse,
)
from ..services import RecommendationEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendation", tags=["Recommendations"])


def get_recommendation_engine() -> RecommendationEngine:
    return RecommendationEngine()


@router.post("/crop", response_model=CropRecommendationResponse, summary="Get crop recommendations")
async def crop_recommendation(
    request: CropRecommendationRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine),
):
    try:
        logger.info(
            "Crop recommendation request: region=%s, year=%d",
            request.region, request.year,
        )
        result = engine.recommend_crops(
            region=request.region,
            year=request.year,
            climate_data=request.climate_data,
        )
        return CropRecommendationResponse(
            region=result["region"],
            year=result["year"],
            recommended_crops=result["recommended_crops"],
            fertilizer_plan=result["fertilizer_plan"],
            irrigation_schedule=result["irrigation_schedule"],
            water_saving_strategies=result["water_saving_strategies"],
            pest_prevention_methods=result["pest_prevention_methods"],
        )
    except ValueError as e:
        logger.warning("Validation error in crop recommendation: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Crop recommendation failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Recommendation service unavailable")


@router.post("/fertilizer", response_model=FertilizerPlanResponse, summary="Get fertilizer recommendations")
async def fertilizer_plan(
    request: FertilizerPlanRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine),
):
    try:
        logger.info(
            "Fertilizer plan request: region=%s, crop=%s, year=%d",
            request.region, request.crop_type, request.year,
        )
        result = engine.generate_fertilizer_plan(
            region=request.region,
            crop_type=request.crop_type,
            year=request.year,
            soil_data=request.soil_data,
        )
        return FertilizerPlanResponse(
            region=result["region"],
            crop_type=result["crop_type"],
            year=result["year"],
            recommended_fertilizers=result["recommended_fertilizers"],
            schedule=result["schedule"],
            total_cost_estimate=result["total_cost_estimate"],
        )
    except ValueError as e:
        logger.warning("Validation error in fertilizer plan: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Fertilizer plan failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Fertilizer plan service unavailable")


@router.post("/irrigation", response_model=IrrigationScheduleResponse, summary="Get irrigation schedule")
async def irrigation_schedule(
    request: IrrigationScheduleRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine),
):
    try:
        logger.info(
            "Irrigation schedule request: region=%s, crop=%s, year=%d",
            request.region, request.crop_type, request.year,
        )
        result = engine.generate_irrigation_schedule(
            region=request.region,
            crop_type=request.crop_type,
            year=request.year,
            climate_data=request.climate_data,
        )
        return IrrigationScheduleResponse(
            region=result["region"],
            crop_type=result["crop_type"],
            year=result["year"],
            schedule=result["schedule"],
            total_water_requirement=result["total_water_requirement"],
            water_saving_strategies=result["water_saving_strategies"],
        )
    except ValueError as e:
        logger.warning("Validation error in irrigation schedule: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Irrigation schedule failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Irrigation schedule service unavailable")
