from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Date,
    func,
)
from sqlalchemy.orm import relationship
from database.engine import Base


class Flight(Base):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    origin_airport_id = Column(Integer, ForeignKey("airport.id"), nullable=False)
    dest_airport_id = Column(Integer, ForeignKey("airport.id"), nullable=False)
    airline_id = Column(Integer, ForeignKey("airline.id"), nullable=False)

    day_of_week = Column(Integer, nullable=False)
    day_of_month = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    fl_date = Column(Date, nullable=False)

    tail_num = Column(String, nullable=False)
    fl_num = Column(Integer, nullable=False)

    # Departure
    crs_dep_time = Column(Integer, nullable=True)
    dep_time = Column(Integer, nullable=True)
    dep_delay = Column(Integer, nullable=True)
    dep_delay_new = Column(Integer, nullable=True)
    dep_del15 = Column(Boolean, nullable=True)
    dep_delay_group = Column(String, nullable=True)
    dep_time_blk = Column(String, nullable=True)
    taxi_out = Column(Integer, nullable=True)
    wheels_off = Column(Integer, nullable=True)
    # Arrival
    wheels_on = Column(Integer, nullable=True)
    taxi_in = Column(Integer, nullable=True)
    crs_arr_time = Column(Integer, nullable=True)
    arr_time = Column(Integer, nullable=True)
    arr_delay = Column(Integer, nullable=True)
    arr_delay_new = Column(Integer, nullable=True)
    arr_delay_group = Column(String, nullable=True)
    arr_time_blk = Column(String, nullable=True)

    # target
    arr_del15 = Column(Boolean, nullable=True)

    created_at = Column(DateTime, default=func.now())

    # relations
    airline = relationship("Airline", back_populates="flights")
    origin_airport = relationship(
        "Airport", foreign_keys=[origin_airport_id], back_populates="origin_flights"
    )
    dest_airport = relationship(
        "Airport", foreign_keys=[dest_airport_id], back_populates="dest_flights"
    )
