from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AirlineBase(BaseModel):
    unique_carrier: str = Field(..., min_length=1, max_length=10)
    airline_id: int = Field(..., min_length=10000, max_length=99999)


class AirlineCreate(AirlineBase):
    pass


class AirlineUpdate(BaseModel):
    unique_carrier: Optional[str] = Field(None, min_length=1, max_length=10)
    airline_id: Optional[int] = Field(None, min_length=10000, max_length=99999)


class AirlineResponse(AirlineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
