# services/prediction_service.py
import mlflow
import pandas as pd
from typing import Dict, Any
from datetime import datetime
from loguru import logger

from models.preprocessor import PreprocessingService
from schemas.prediction import PredictionRequest
from models.model_loader import ModelLoader
# from database.metrics_client import MetricsClient


class PredictionService:
    def __init__(self):
        self.preprocessor = PreprocessingService()
        self.model_loader = ModelLoader()
        # self.metrics_client = MetricsClient()

    async def predict(self, data: PredictionRequest) -> Dict[str, Any]:
        try:
            # 1. Chargement du modèle et preprocessor depuis MLflow
            model_info = self.model_loader.load_latest_model()
            model = model_info["model"]
            preprocessor = model_info["preprocessor"]

            # 2. Préprocessing des données (features seulement)
            processed_data = preprocessor.transform_features(data.model_dump())

            # 3. Prédiction
            prediction = model.predict(processed_data)
            probability = model.predict_proba(processed_data)

            # 4. Interpréter la prédiction
            prediction_label = preprocessor.inverse_transform_target(prediction)

            # 5. Logging de la prédiction
            await self._log_prediction(data, prediction_label, probability)

            logger.debug(f"prediction label: {prediction_label[0]}")

            return {
                "prediction": prediction_label[0],  # ">=50K" ou "<50K"
                "prediction_binary": int(prediction[0]),  # 0 ou 1
                "probability": float(probability[0][1]),
                "model_version": model_info["version"],
            }

        except Exception as err:
            raise Exception(str(err))

    async def _log_prediction(self, input_data, prediction, probability):
        # # Log pour monitoring et drift detection
        # prediction_log = {
        #     "input_data": input_data.model_dump(),
        #     "prediction": prediction[0],
        #     "probability": probability[0].tolist(),
        #     "timestamp": datetime.utcnow(),
        # }
        # await self.metrics_client.log_prediction(prediction_log)
        pass
