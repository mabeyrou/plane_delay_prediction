import mlflow
import mlflow.sklearn
from typing import Dict, Any


class ModelLoader:
    def __init__(self):
        self.current_model = None
        self.current_preprocessor = None
        self.current_version = None

    def load_latest_model(self) -> Dict[str, Any]:
        """Charge le dernier modèle depuis MLflow"""
        try:
            # Récupérer le dernier modèle en production
            client = mlflow.tracking.MlflowClient()
            model_version = client.get_latest_versions(
                "revenue_prediction_model", stages=["Production"]
            )[0]

            # Charger le modèle
            model_uri = f"models:/revenue_prediction_model/{model_version.version}"
            model = mlflow.sklearn.load_model(model_uri)

            # Charger le preprocessor
            preprocessor_uri = (
                f"models:/revenue_prediction_model/{model_version.version}/preprocessor"
            )
            preprocessor = mlflow.sklearn.load_model(preprocessor_uri)

            # Mettre en cache
            self.current_model = model
            self.current_preprocessor = preprocessor
            self.current_version = model_version.version

            return {
                "model": model,
                "preprocessor": preprocessor,
                "version": model_version.version,
            }

        except Exception as e:
            # Fallback vers le modèle en cache si disponible
            if self.current_model is not None:
                return {
                    "model": self.current_model,
                    "preprocessor": self.current_preprocessor,
                    "version": self.current_version,
                }
            else:
                raise ValueError(f"No model available: {str(e)}")

    def load_model_by_version(self, version: str) -> Dict[str, Any]:
        """Charge un modèle spécifique par version"""
        model_uri = f"models:/revenue_prediction_model/{version}"
        model = mlflow.sklearn.load_model(model_uri)

        preprocessor_uri = f"models:/revenue_prediction_model/{version}/preprocessor"
        preprocessor = mlflow.sklearn.load_model(preprocessor_uri)

        return {"model": model, "preprocessor": preprocessor, "version": version}
