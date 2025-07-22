from dotenv import load_dotenv
from os import getenv

load_dotenv()

APP_ENV = getenv("APP_ENV", "development")

POSTGRES_USER = getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = getenv("POSTGRES_DB", "appdb")
POSTGRES_PORT = getenv("POSTGRES_PORT", 5432)

DATABASE_URL = getenv("DATABASE_URL", "")

LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")
