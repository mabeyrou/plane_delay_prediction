from fastapi import APIRouter
import pandas as pd
from models import prediction
from schemas.prediction import FlightPredictionRequest

router = APIRouter()


@router.post("/predict")
async def predict(prediction_request: FlightPredictionRequest):
    try:
        model = prediction.load_latest_model()

        data_dict = prediction_request.model_dump()

        input_df = pd.DataFrame([data_dict])

        predictions = model.predict(input_df)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)
            return {
                "prediction": int(predictions[0]),
                "probability": float(probabilities[0][1]),  # Probabilité de retard
            }
        else:
            return {"prediction": int(predictions[0])}
    except Exception as err:
        return {"error": str(err)}
