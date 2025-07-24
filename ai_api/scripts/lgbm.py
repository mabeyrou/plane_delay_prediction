from models.preprocessor import create_preprocessor, split_data
from models.training import create_model, train_model_with_validation
from sklearn.metrics import accuracy_score, classification_report
import mlflow
from os.path import join
import pandas as pd

raw_data_path = join("data")
sample_100000_path = join(raw_data_path, "balanced_sample_100000.parquet")
df = pd.read_parquet(sample_100000_path)

features = [
    "MONTH",
    "DAY_OF_MONTH",
    "DAY_OF_WEEK",
    "UNIQUE_CARRIER",
    "ORIGIN",
    "DEST",
    "CRS_DEP_TIME",
    "DEP_TIME",
    "DEP_DELAY",
    "TAXI_OUT",
    "WHEELS_OFF",
    "CRS_ARR_TIME",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
]
target = ["ARR_DEL15"]

cat_features = ["UNIQUE_CARRIER", "ORIGIN", "DEST"]
num_features = [feat for feat in features if feat not in cat_features]

X = df[features]
y = df[target]

X_train_full, X_test, y_train_full, y_test = split_data(X, y, test_size=0.2)

X_train, X_val, y_train, y_val = split_data(X_train_full, y_train_full, test_size=0.25)

print(f"Taille du jeu d'entraînement: {len(X_train)}")
print(f"Taille du jeu de validation: {len(X_val)}")
print(f"Taille du jeu de test: {len(X_test)}")

preprocessor = create_preprocessor(num_features, cat_features)
learning_rate = 0.1
n_estimators = 300
num_leaves = 31
objective = "binary"
metric = "binary_logloss"

pipeline = create_model(
    preprocessor, learning_rate, n_estimators, num_leaves, objective, metric
)

trained_pipeline = train_model_with_validation(pipeline, X_train, y_train, X_val, y_val)

print("\nModèle entraîné et loggué dans MLflow avec les courbes de loss.")

# --- ÉTAPE FINALE : ÉVALUATION SUR LE JEU DE TEST INTENTIONNELLEMENT MIS DE CÔTÉ ---
print("\n--- Évaluation finale sur le jeu de test ---")

# 1. Faire des prédictions sur les données de test BRUTES.
# La pipeline s'occupe du pré-traitement.
test_predictions = trained_pipeline.predict(X_test)

# 2. Calculer les métriques de performance.
accuracy = accuracy_score(y_test, test_predictions)
report = classification_report(y_test, test_predictions)

print(f"Précision sur le jeu de test : {accuracy:.4f}")
print("\nRapport de classification sur le jeu de test :")
print(report)

# 3. (Optionnel mais recommandé) Logguer ces métriques finales dans le même run MLflow.
# Pour cela, il faut récupérer le run_id ou être dans le contexte du run.
# La façon la plus simple est de le faire à l'intérieur de la fonction d'entraînement.

# Voici une version modifiée de `train_model_with_validation` qui le ferait :
# (à mettre dans training.py)
#
# def train_model_with_validation(...):
#     ...
#     with mlflow.start_run(...) as run:
#         ...
#         classifier.fit(...)
#
#         # Évaluation sur le test APRES l'entraînement
#         test_predictions = pipeline.predict(X_test) # pipeline a le classifieur entraîné
#         test_accuracy = accuracy_score(y_test, test_predictions)
#         mlflow.log_metric("test_accuracy", test_accuracy)
#
#     return pipeline
