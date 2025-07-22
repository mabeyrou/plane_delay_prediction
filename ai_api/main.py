from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from routes import health, model
from config import APP_ENV

app = FastAPI()
app.include_router(health.router)
app.include_router(model.router)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

logger.remove()

logger.add(
    f"./logs/{APP_ENV}_ai_api.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="TRACE",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
