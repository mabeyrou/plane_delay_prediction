from loguru import logger
import pandas as pd
from os.path import join
import asyncio

from models.fetching_data import fetch_all_profiles_from_api
from models.training import TrainingService
from schemas.training_config import ModelType, TrainingConfig

# df = fetch_all_profiles_from_api() # A décommenter quand j'aurais le process pour nettoyer les données
df_path = join("data", "preprocessed_data.csv")
df = pd.read_csv(df_path)

cols_to_drop = ["created_at", "id"]

df = df.dropna()
df = df.drop(columns=cols_to_drop)


async def main():
    trainingService = TrainingService()

    model_type = ModelType.RANDOM_FOREST
    trainingConfig = TrainingConfig(
        model_type=model_type,
        hyperparameters={"n_estimators": 100, "max_depth": 10, "random_state": 42},
        data_path=df_path,
        experiment_name=f"revenue_prediction_{model_type}",
    )

    await trainingService.train_model(trainingConfig)


if __name__ == "__main__":
    asyncio.run(main())
