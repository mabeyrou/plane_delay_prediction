from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import tempfile
import mlflow
from mlflow.models.signature import infer_signature
import os
from config import MLFLOW_BACKEND_STORE_URI
import matplotlib.pyplot as plt
import seaborn as sns


def create_model(
    preprocessor,
    learning_rate=0.1,
    n_estimators=300,
    num_leaves=31,
    objective="binary",
    metric="binary_logloss",
    random_state=42,
):
    """
    Crée le modèle LightGBM avec la pipeline de preprocessing.
    Les hyperparamètres par défaut correspondent à ceux issus de la cross-validation.
    """
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
    X_test=None,
    y_test=None,
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
        classifier.fit(
            X_train_processed,
            y_train.values.ravel(),
            eval_set=[(X_val_processed, y_val.values.ravel())],
            eval_metric="logloss",
            callbacks=[lgb.early_stopping(10, verbose=False)],
        )

        signature = infer_signature(X_train, pipeline.predict(X_train))
        mlflow.lightgbm.log_model(pipeline, artifact_path="model", signature=signature)

        # Train
        y_train_pred = classifier.predict(X_train_processed)
        y_train_proba = (
            classifier.predict_proba(X_train_processed)[:, 1]
            if hasattr(classifier, "predict_proba")
            else None
        )
        log_metrics_and_reports(y_train, y_train_pred, y_train_proba, "train")

        # Validation
        y_val_pred = classifier.predict(X_val_processed)
        y_val_proba = (
            classifier.predict_proba(X_val_processed)[:, 1]
            if hasattr(classifier, "predict_proba")
            else None
        )
        log_metrics_and_reports(y_val, y_val_pred, y_val_proba, "val")

        # Test
        if X_test is not None and y_test is not None:
            X_test_processed = preprocessor.transform(X_test)
            test_predictions = classifier.predict(X_test_processed)
            test_proba = (
                classifier.predict_proba(X_test_processed)[:, 1]
                if hasattr(classifier, "predict_proba")
                else None
            )
            log_metrics_and_reports(y_test, test_predictions, test_proba, "test")

        run_id = run.info.run_id
        print(f"MLflow Run completed with run_id {run_id}")

    return pipeline


def log_metrics_and_reports(
    y_true, y_pred, y_proba, step_name, artifact_path="reports"
):
    """
    Loggue classification reports, matrices de confusion et métriques dans MLflow.
    """
    # Classification report
    report = classification_report(y_true, y_pred, output_dict=False)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tmp_file:
        tmp_file.write(report)
        tmp_path = tmp_file.name
    mlflow.log_artifact(
        tmp_path, artifact_path=f"{artifact_path}/{step_name}_classification_report"
    )
    os.remove(tmp_path)

    # Matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {step_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
        plt.savefig(img_file.name)
        mlflow.log_artifact(
            img_file.name, artifact_path=f"{artifact_path}/{step_name}_confusion_matrix"
        )
        plt.close()
        os.remove(img_file.name)

    # Métriques individuelles
    mlflow.log_metric(f"{step_name}_accuracy", accuracy_score(y_true, y_pred))
    mlflow.log_metric(f"{step_name}_precision", precision_score(y_true, y_pred))
    mlflow.log_metric(f"{step_name}_recall", recall_score(y_true, y_pred))
    mlflow.log_metric(f"{step_name}_f1", f1_score(y_true, y_pred))
    if y_proba is not None:
        try:
            mlflow.log_metric(f"{step_name}_roc_auc", roc_auc_score(y_true, y_proba))
        except Exception:
            pass
