from crud.base import CRUDBase
from models.flight import Flight
from schemas.flight import FlightCreate, FlightUpdate


flight_crud = CRUDBase[Flight, FlightCreate, FlightUpdate](Flight)
