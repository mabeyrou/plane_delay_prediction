from dotenv import load_dotenv
from os import getenv

load_dotenv()

APP_ENV = getenv("APP_ENV", "development")

LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")

DATA_API_URL = getenv("DATA_API_URL", "http://data_api:8001/")

MLFLOW_BACKEND_STORE_URI = getenv("MLFLOW_BACKEND_STORE_URI", "file:///app/mlruns")
