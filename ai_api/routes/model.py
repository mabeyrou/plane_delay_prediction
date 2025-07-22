from fastapi import APIRouter

from schemas.prediction import PredictionRequest

router = APIRouter()


@router.post("/predict")
async def predict(prediction_request: PredictionRequest):
    pass
