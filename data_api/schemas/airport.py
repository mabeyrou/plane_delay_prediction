from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AirportBase(BaseModel):
    iata_code: str = Field(..., min_length=3, max_length=3)
    airport_tech_id: int = Field(..., ge=10000, le=99999)
    airport_seq_id: int = Field(..., ge=1000000, le=9999999)
    city_market_id: int = Field(..., ge=10000, le=99999)
    city_name: str = Field(..., min_length=1, max_length=100)
    state_abr: str = Field(..., min_length=1, max_length=10)
    state_fips: int = Field(..., ge=1, le=100)
    state_name: str = Field(..., min_length=1, max_length=100)
    wac_code: int = Field(..., ge=1, le=100)


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    iata_code: Optional[str] = Field(None, min_length=3, max_length=3)
    airport_tech_id: Optional[int] = Field(None, ge=10000, le=99999)
    airport_seq_id: Optional[int] = Field(None, ge=1000000, le=9999999)
    city_market_id: Optional[int] = Field(None, ge=10000, le=99999)
    city_name: Optional[str] = Field(None, min_length=1, max_length=100)
    state_abr: Optional[str] = Field(None, min_length=1, max_length=10)
    state_fips: Optional[int] = Field(None, ge=1, le=100)
    state_name: Optional[str] = Field(None, min_length=1, max_length=100)
    wac_code: Optional[int] = Field(None, ge=1, le=100)


class AirportResponse(AirportBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
