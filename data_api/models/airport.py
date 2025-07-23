from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from database.engine import Base


class Airport(Base):
    __tablename__ = "airport"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    iata_code = Column(String, nullable=False, unique=True)
    airport_tech_id = Column(Integer, nullable=False, unique=True)
    airport_seq_id = Column(Integer, nullable=False, unique=True)
    city_market_id = Column(Integer, nullable=False)
    city_name = Column(String, nullable=False)
    state_abr = Column(String, nullable=False)
    state_fips = Column(Integer, nullable=False)
    state_name = Column(String, nullable=False)
    wac_code = Column(Integer, nullable=False)

    origin_flights = relationship(
        "Flight",
        foreign_keys="[Flight.origin_airport_id]",
        back_populates="origin_airport",
    )
    dest_flights = relationship(
        "Flight", foreign_keys="[Flight.dest_airport_id]", back_populates="dest_airport"
    )
