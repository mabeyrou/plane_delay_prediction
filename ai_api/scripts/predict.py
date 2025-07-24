import pandas as pd
import mlflow
from config import MLFLOW_BACKEND_STORE_URI

EXPERIMENT_NAME = "lgbm_plane_delay_prediction"
mlflow.set_tracking_uri(MLFLOW_BACKEND_STORE_URI)
runs = mlflow.search_runs(
    experiment_names=[EXPERIMENT_NAME], order_by=["attributes.start_time DESC"]
)

if runs.shape[0] == 0:
    raise RuntimeError(f"Aucun run trouvé pour l'expérience '{EXPERIMENT_NAME}'.")

latest_run_id = runs.iloc[0]["run_id"]
model_uri = f"runs:/{latest_run_id}/model"

print(f"Chargement du modèle MLflow depuis : {model_uri}")

model = mlflow.lightgbm.load_model(model_uri)

sample_data = pd.DataFrame(
    {
        "MONTH": [7, 3],
        "DAY_OF_MONTH": [15, 1],
        "DAY_OF_WEEK": [3, 1],
        "UNIQUE_CARRIER": ["AA", "AA"],
        "ORIGIN": ["JFK", "LAX"],
        "DEST": ["LAX", "SFO"],
        "CRS_DEP_TIME": [900, 1000],
        "DEP_TIME": [905, 1000],
        "DEP_DELAY": [5.0, 30.0],
        "TAXI_OUT": [12.0, 5.0],
        "WHEELS_OFF": [917, 1035],
        "CRS_ARR_TIME": [1200, 1300],
        "CRS_ELAPSED_TIME": [180.0, 200.0],
        "DISTANCE": [2475.0, 3521.0],
    }
)

pred = model.predict(sample_data)
print("Prédiction :", pred)
