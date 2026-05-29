import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query

from ..schemas import (
    DiseaseRiskRequest,
    DiseaseRiskResponse,
    DiseaseBatchResponse,
)
from ..services import DiseasePredictor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/disease", tags=["Diseases"])


def get_disease_predictor() -> DiseasePredictor:
    return DiseasePredictor()


@router.post("/risk", response_model=DiseaseRiskResponse, summary="Predict disease and pest risk")
async def disease_risk(
    request: DiseaseRiskRequest,
    predictor: DiseasePredictor = Depends(get_disease_predictor),
):
    try:
        logger.info(
            "Disease risk request: region=%s, crop=%s, year=%d",
            request.region, request.crop_type, request.year,
        )
        result = predictor.predict_risk(
            region=request.region,
            crop_type=request.crop_type,
            year=request.year,
        )
        return DiseaseRiskResponse(
            region=result["region"],
            crop_type=result["crop_type"],
            year=result["year"],
            pest_attack_probability=result["pest_attack_probability"],
            disease_outbreak_probability=result["disease_outbreak_probability"],
            seasonal_risk=result["seasonal_risk"],
            preventive_measures=result["preventive_measures"],
        )
    except ValueError as e:
        logger.warning("Validation error in disease risk: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Disease risk prediction failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Disease prediction service unavailable")


@router.post("/batch", response_model=DiseaseBatchResponse, summary="Batch disease predictions")
async def disease_batch(
    requests: List[DiseaseRiskRequest],
    predictor: DiseasePredictor = Depends(get_disease_predictor),
):
    try:
        logger.info("Batch disease risk request for %d items", len(requests))
        payloads = [
            {
                "region": r.region,
                "crop_type": r.crop_type,
                "year": r.year,
            }
            for r in requests
        ]
        results = predictor.predict_batch(payloads)
        predictions = []
        successful = 0
        failed = 0
        for res in results:
            if res["status"] == "success":
                d = res["data"]
                predictions.append(
                    DiseaseRiskResponse(
                        region=d["region"],
                        crop_type=d["crop_type"],
                        year=d["year"],
                        pest_attack_probability=d["pest_attack_probability"],
                        disease_outbreak_probability=d["disease_outbreak_probability"],
                        seasonal_risk=d["seasonal_risk"],
                        preventive_measures=d["preventive_measures"],
                    )
                )
                successful += 1
            else:
                failed += 1
        logger.info("Batch disease risk complete: %d success, %d failed", successful, failed)
        return DiseaseBatchResponse(
            results=predictions,
            total=len(requests),
            successful=successful,
            failed=failed,
        )
    except Exception as e:
        logger.error("Batch disease prediction failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Batch disease prediction service unavailable")


@router.get("/history/{region}", response_model=List[DiseaseRiskResponse], summary="Get historical disease data for a region")
async def disease_history(
    region: str,
    limit: int = Query(100, ge=1, le=1000),
    predictor: DiseasePredictor = Depends(get_disease_predictor),
):
    try:
        logger.info("Disease history request: region=%s, limit=%d", region, limit)
        history = predictor.get_disease_history(region=region, limit=limit)
        return [
            DiseaseRiskResponse(
                region=h["region"],
                crop_type=h["crop_type"],
                year=h["year"],
                pest_attack_probability=h["pest_attack_probability"],
                disease_outbreak_probability=h["disease_outbreak_probability"],
                seasonal_risk=h["seasonal_risk"],
                preventive_measures=h["preventive_measures"],
            )
            for h in history
        ]
    except Exception as e:
        logger.error("Disease history fetch failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch disease history")
