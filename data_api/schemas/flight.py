from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from schemas.airline import AirlineResponse
from schemas.airport import AirportResponse


class FlightBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    day_of_week: int = Field(..., ge=1, le=7)
    day_of_month: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)
    quarter: int = Field(..., ge=1, le=4)
    fl_date: date = Field(...)

    tail_num: str = Field(..., min_length=1, max_length=100)
    fl_num: int = Field(..., ge=1, le=1000)

    crs_dep_time: int = Field(...)
    dep_time: int = Field(...)
    dep_delay: int = Field(...)
    dep_delay_new: int = Field(...)
    dep_del15: bool = Field(...)
    dep_delay_group: str = Field(..., min_length=1, max_length=100)
    dep_time_blk: str = Field(..., min_length=1, max_length=100)
    taxi_out: int = Field(...)
    wheels_off: int = Field(...)

    wheels_on: int = Field(...)
    taxi_in: int = Field(...)
    crs_arr_time: int = Field(...)
    arr_time: int = Field(...)
    arr_delay: int = Field(...)
    arr_delay_new: int = Field(...)
    arr_delay_group: str = Field(..., min_length=1, max_length=100)
    arr_time_blk: str = Field(..., min_length=1, max_length=100)


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    day_of_week: Optional[int] = Field(None, ge=1, le=7)
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    month: Optional[int] = Field(None, ge=1, le=12)
    year: Optional[int] = Field(None, ge=2000)
    quarter: Optional[int] = Field(None, ge=1, le=4)
    fl_date: Optional[date] = Field(None)

    tail_num: Optional[str] = Field(None, min_length=1, max_length=100)
    fl_num: Optional[int] = Field(None, ge=1, le=1000)

    crs_dep_time: Optional[int] = Field(None)
    dep_time: Optional[int] = Field(None)
    dep_delay: Optional[int] = Field(None)
    dep_delay_new: Optional[int] = Field(None)
    dep_del15: Optional[bool] = Field(None)
    dep_delay_group: Optional[str] = Field(None, min_length=1, max_length=100)
    dep_time_blk: Optional[str] = Field(None, min_length=1, max_length=100)
    taxi_out: Optional[int] = Field(None)
    wheels_off: Optional[int] = Field(None)

    wheels_on: Optional[int] = Field(None)
    taxi_in: Optional[int] = Field(None)
    crs_arr_time: Optional[int] = Field(None)
    arr_time: Optional[int] = Field(None)
    arr_delay: Optional[int] = Field(None)
    arr_delay_new: Optional[int] = Field(None)
    arr_delay_group: Optional[str] = Field(None, min_length=1, max_length=100)
    arr_time_blk: Optional[str] = Field(None, min_length=1, max_length=100)


class FlightResponse(FlightBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    day_of_week: int
    day_of_month: int
    month: int
    year: int
    quarter: int
    fl_date: date

    tail_num: str
    fl_num: int

    crs_dep_time: int
    dep_time: int
    dep_delay: int
    dep_delay_new: int
    dep_del15: bool
    dep_delay_group: str
    dep_time_blk: str
    taxi_out: int
    wheels_off: int

    wheels_on: int
    taxi_in: int
    crs_arr_time: int
    arr_time: int
    arr_delay: int
    arr_delay_new: int
    arr_delay_group: str
    arr_time_blk: str

    airline: AirlineResponse
    airport: AirportResponse

    created_at: datetime


class FlightForML(FlightBase):
    day_of_week: int
    day_of_month: int
    month: int

    tail_num: str
    fl_num: int

    crs_dep_time: int
    dep_time: int
    dep_delay_new: int
    dep_del15: bool
    dep_delay_group: str
    dep_time_blk: str
    taxi_out: int
    wheels_off: int

    airline_id: int
    airport_id: int
