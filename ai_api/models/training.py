import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from typing import Dict, Any
from loguru import logger
import pandas as pd
from os.path import join
# from datetime import datetime

from models.preprocessor import PreprocessingService
from schemas.training_config import TrainingConfig, ModelType
from config import MLFLOW_BACKEND_STORE_URI
# from database.metrics_client import MetricsClient


class TrainingService:
    def __init__(self):
        mlflow.set_tracking_uri(MLFLOW_BACKEND_STORE_URI)
        mlflow.set_experiment("Income prediction experiment")

    async def train_model(self, config: TrainingConfig) -> Dict[str, Any]:
        with mlflow.start_run() as run:
            try:
                data = self._load_training_data(config.data_path)

                preprocessor = PreprocessingService()
                X_processed, y = preprocessor.fit_transform(data)

                X_train, X_test, y_train, y_test = train_test_split(
                    X_processed, y, test_size=0.2, random_state=42, stratify=y
                )

                model = self._create_model(config.model_type, config.hyperparameters)
                model.fit(X_train, y_train)

                metrics = self._evaluate_model(model, X_test, y_test)

                # Log des paramètres et métriques
                mlflow.log_params(config.hyperparameters)
                for k, v in metrics.items():
                    mlflow.log_metric(k, v)

                # Log du modèle
                mlflow.sklearn.log_model(model, "model")

                # Log du préprocesseur
                mlflow.sklearn.log_model(preprocessor, "preprocessor")

                # Enregistrement dans le Model Registry
                mlflow.register_model(
                    f"runs:/{run.info.run_id}/model",
                    "revenue_prediction_model"
                )
                mlflow.register_model(
                    f"runs:/{run.info.run_id}/preprocessor",
                    "revenue_prediction_preprocessor"
                )

                return {
                    "run_id": run.info.run_id,
                    "metrics": metrics,
                    "model_uri": f"runs:/{run.info.run_id}/model",
                }

            except Exception as err:
                mlflow.log_param("status", "failed")
                mlflow.log_param("error", str(err))
                raise Exception(str(err))

    def _load_training_data(self, data_path: str):
        df = pd.read_csv(data_path)

        cols_to_drop = ["created_at", "id", "was_used_for_training"]

        df = df.dropna()
        df = df.drop(columns=cols_to_drop)

        return df

    def _create_model(self, model_type: ModelType, hyperparameters: Dict):
        if model_type == "random_forest":
            return RandomForestClassifier(**hyperparameters)
        elif model_type == "logistic_regression":
            return LogisticRegression(**hyperparameters)
        else:
            raise ValueError(f"Model type {model_type} not supported")

    def _evaluate_model(self, model, X_test, y_test) -> Dict[str, float]:
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_pred_proba),
        }

    async def _save_metrics_to_db(self, run_id: str, metrics: Dict[str, float]):
        logger.info(f"run id: {run_id}")
        logger.info(f"metrics: {metrics}")
        # model_metrics = {
        #     "run_id": run_id,
        #     "metrics": metrics,
        #     "created_at": datetime.utcnow(),
        #     "model_status": "trained",
        # }
        # await self.metrics_client.save_model_metrics(model_metrics)
        pass
