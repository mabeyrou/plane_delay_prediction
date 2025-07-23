from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AirportBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class AirportResponse(AirportBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
