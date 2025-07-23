from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from database.engine import Base


class Airline(Base):
    __tablename__ = "airline"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    unique_carrier = Column(String, nullable=False, unique=True)
    airline_id = Column(String, nullable=False, unique=True)

    flights = relationship("Flight", back_populates="airline")
