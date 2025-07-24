from pydantic import BaseModel, Field
from typing import Optional


class FlightPredictionRequest(BaseModel):
    MONTH: int = Field(..., ge=1, le=12)
    DAY_OF_MONTH: int = Field(..., ge=1, le=31)
    DAY_OF_WEEK: int = Field(..., ge=1, le=7)
    UNIQUE_CARRIER: str = Field(...)
    ORIGIN: str = Field(..., min_length=3, max_length=3)
    DEST: str = Field(..., min_length=3, max_length=3)
    CRS_DEP_TIME: int = Field(..., ge=0, le=2359)
    DEP_TIME: int = Field(..., ge=0, le=2359)
    DEP_DELAY: float = Field(...)
    TAXI_OUT: float = Field(..., ge=0)
    WHEELS_OFF: int = Field(..., ge=0, le=2359)
    CRS_ARR_TIME: int = Field(..., ge=0, le=2359)
    CRS_ELAPSED_TIME: float = Field(..., ge=0)
    DISTANCE: float = Field(..., ge=0)


class PredictionResponse(BaseModel):
    prediction: int = Field(...)
    probability: Optional[float] = Field(None)
