# data_processing/preprocessor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from typing import Dict


class PreprocessingService:
    def __init__(self):
        self.pipeline = None
        self.target_encoder = LabelEncoder()
        self.feature_names = None

    def fit_transform(self, data: pd.DataFrame) -> tuple:
        """Fit le preprocessor et transforme les données d'entraînement"""
        X = data.drop("income", axis=1)
        y = data["income"]

        y_encoded = self.target_encoder.fit_transform(y)

        numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                ("onehot", OneHotEncoder(drop="first", sparse_output=False)),
            ]
        )

        self.pipeline = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ],
            remainder="passthrough",
        )

        X_processed = self.pipeline.fit_transform(X)

        self.feature_names = self._get_feature_names()

        return X_processed, y_encoded

    def transform(self, data: Dict) -> np.ndarray:
        """Transforme les données de prédiction"""
        if self.pipeline is None:
            raise ValueError("Preprocessor not fitted yet")

        df = pd.DataFrame([data])

        X_processed = self.pipeline.transform(df)

        return X_processed

    def inverse_transform_target(self, target_encoded: np.ndarray) -> np.ndarray:
        """Inverse transform de la target (pour interpréter les prédictions)"""
        if not self.fitted:
            raise ValueError("Preprocessor not fitted yet. Call fit() first.")

        return self.target_encoder.inverse_transform(target_encoded)

    def _get_feature_names(self) -> list:
        """Récupère les noms des features après preprocessing"""
        feature_names = []
        for name, transformer, features in self.pipeline.transformers_:
            if name == "num":
                feature_names.extend(features)
            elif name == "cat":
                if hasattr(transformer.named_steps["onehot"], "get_feature_names_out"):
                    cat_features = transformer.named_steps[
                        "onehot"
                    ].get_feature_names_out(features)
                    feature_names.extend(cat_features)
        return feature_names
