import pandas as pd
import mlflow
import mlflow.sklearn


def load_model(model_uri):
    """Charge un modèle MLflow."""
    loaded_model = mlflow.sklearn.load_model(model_uri)
    return loaded_model


def predict(model, data):
    """Effectue des prédictions avec le modèle chargé."""
    predictions = model.predict(data)
    return predictions


if __name__ == "__main__":
    # Exemple d'utilisation (à adapter avec tes données)
    import pandas as pd
    from preprocessing import prepare_data, create_preprocessing_pipeline

    # Création des données d'exemple
    data = {
        "num1": [1, 2, 3, 4, 5],
        "cat1": ["A", "B", "A", "C", "B"],
        "target": [0, 1, 0, 1, 0],
    }
    df = pd.DataFrame(data)
    features = ["num1", "cat1"]
    target = ["target"]
    cat_features = ["cat1"]
    num_features = ["num1"]

    # Préparation des données
    X_train, X_test, y_train, y_test = prepare_data(df, features, target, cat_features)
    preprocessor = create_preprocessing_pipeline(num_features, cat_features)
    X_test_processed = preprocessor.transform(X_test)  # Use transform instead of fit_transform

    # Remplace avec l'URI de ton modèle MLflow
    model_uri = "runs:/<YOUR_RUN_ID>/model"  # Remplace <YOUR_RUN_ID> par l'ID de ta run MLflow

    # Chargement du modèle
    loaded_model = load_model(model_uri)

    # Prédiction
    predictions = predict(loaded_model, X_test)
    print("Predictions:", predictions)