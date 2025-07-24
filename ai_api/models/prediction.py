import pandas as pd
import mlflow
from config import MLFLOW_BACKEND_STORE_URI

EXPERIMENT_NAME = "lgbm_plane_delay_prediction"


def load_latest_model(model_uri):
    """Charge le dernier modèle MLflow."""
    mlflow.set_tracking_uri(MLFLOW_BACKEND_STORE_URI)
    runs = mlflow.search_runs(
        experiment_names=[EXPERIMENT_NAME], order_by=["attributes.start_time DESC"]
    )

    if runs.shape[0] == 0:
        raise RuntimeError(f"Aucun run trouvé pour l'expérience '{EXPERIMENT_NAME}'.")

    latest_run_id = runs.iloc[0]["run_id"]
    model_uri = f"runs:/{latest_run_id}/model"

    print(f"Chargement du modèle MLflow depuis : {model_uri}")

    return mlflow.lightgbm.load_model(model_uri)


def predict(model, data):
    """Effectue des prédictions avec le modèle chargé."""
    predictions = model.predict(data)
    return predictions
