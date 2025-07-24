import lightgbm as lgb
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.lightgbm
from config import MLFLOW_BACKEND_STORE_URI


def create_model(
    preprocessor,
    learning_rate,
    n_estimators,
    num_leaves,
    objective,
    metric,
    random_state=42,
):
    """Crée le modèle LightGBM avec la pipeline de preprocessing."""
    lgbm = lgb.LGBMClassifier(
        random_state=random_state,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        num_leaves=num_leaves,
        objective=objective,
        metric=metric,
    )

    full_pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", lgbm)])
    return full_pipeline


def train_model_with_validation(
    pipeline,
    X_train,
    y_train,
    X_val,
    y_val,
    experiment_name="lgbm_plane_delay_prediction",
    run_name="LightGBM Training with Validation",
):
    """
    Pré-traite les données, entraîne le modèle avec un jeu de validation,
    et enregistre tout avec MLflow autolog.
    """
    mlflow.set_tracking_uri(MLFLOW_BACKEND_STORE_URI)
    mlflow.set_experiment(experiment_name)

    preprocessor = pipeline.named_steps["preprocessor"]
    X_train_processed = preprocessor.fit_transform(X_train)
    X_val_processed = preprocessor.transform(X_val)

    classifier = pipeline.named_steps["classifier"]

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.lightgbm.autolog()

        classifier.fit(
            X_train_processed,
            y_train.values.ravel(),
            eval_set=[(X_val_processed, y_val.values.ravel())],
            eval_metric="logloss",
            callbacks=[lgb.early_stopping(10, verbose=False)],
        )

        run_id = run.info.run_id
        print(f"MLflow Run completed with run_id {run_id}")

    return pipeline
