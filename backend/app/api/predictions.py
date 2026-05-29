import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from ..schemas import (
    PredictRequest,
    PredictResponse,
    BatchPredictResponse,
)
from ..services import MLPipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["Predictions"])


def get_ml_pipeline() -> MLPipeline:
    return MLPipeline()


@router.post("", response_model=PredictResponse, summary="Make a single crop yield prediction")
async def predict_yield(
    request: PredictRequest,
    pipeline: MLPipeline = Depends(get_ml_pipeline),
):
    try:
        logger.info(
            "Prediction request: year=%d, item=%s, region=%.2f",
            request.Year, request.item, request.area,
        )
        result = pipeline.predict(
            year=request.Year,
            avg_rainfall=request.avg_rainfall,
            pesticides=request.pesticides,
            avg_temp=request.avg_temp,
            area=request.area,
            item=request.item,
        )
        return PredictResponse(
            predicted_yield=result["predicted_yield"],
            item=result["item"],
            year=result["year"],
            confidence=result.get("confidence"),
        )
    except ValueError as e:
        logger.warning("Validation error in prediction: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Prediction failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction service unavailable")


@router.post("/batch", response_model=BatchPredictResponse, summary="Batch crop yield predictions")
async def batch_predict(
    requests: List[PredictRequest],
    pipeline: MLPipeline = Depends(get_ml_pipeline),
):
    try:
        logger.info("Batch prediction request for %d items", len(requests))
        payloads = [
            {
                "Year": r.Year,
                "avg_rainfall": r.avg_rainfall,
                "pesticides": r.pesticides,
                "avg_temp": r.avg_temp,
                "area": r.area,
                "item": r.item,
            }
            for r in requests
        ]
        results = pipeline.predict_batch(payloads)
        predictions = []
        successful = 0
        failed = 0
        for res in results:
            if res["status"] == "success":
                d = res["data"]
                predictions.append(
                    PredictResponse(
                        predicted_yield=d["predicted_yield"],
                        item=d["item"],
                        year=d["year"],
                        confidence=d.get("confidence"),
                    )
                )
                successful += 1
            else:
                failed += 1
        logger.info("Batch complete: %d success, %d failed", successful, failed)
        return BatchPredictResponse(
            predictions=predictions,
            total=len(requests),
            successful=successful,
            failed=failed,
        )
    except Exception as e:
        logger.error("Batch prediction failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Batch prediction service unavailable")
