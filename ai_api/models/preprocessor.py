import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def create_preprocessor(num_features, cat_features):
    """
    Crée un ColumnTransformer pour pré-traiter les features numériques et catégorielles.
    """
    num_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]
    )

    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        [("num", num_pipeline, num_features), ("cat", cat_pipeline, cat_features)],
        remainder="passthrough",
    )

    return preprocessor


def split_data(features, target, test_size=0.2, random_state=42):
    """
    Divise les données en ensembles d'entraînement et de test.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test
