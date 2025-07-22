from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from config import APP_ENV
from database.engine import create_db_tables
from routes import (
    health,
    education,
    income,
    marital_status,
    occupation,
    soc_dem_profile,
    workclass,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Creating database tables if they don't exist...")
    try:
        create_db_tables()
        logger.info("Database tables checked/created successfully.")
    except Exception as err:
        logger.error(f"Failed to create database tables: {err}")
        raise

    yield

    logger.info("Application shutdown: Cleaning up resources...")


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

logger.remove()

logger.add(
    f"./logs/{APP_ENV}_data_api.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="TRACE",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
