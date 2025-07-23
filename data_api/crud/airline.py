from crud.base import CRUDBase
from models.airline import Airline
from schemas.airline import AirlineCreate, AirlineUpdate


airline_crud = CRUDBase[Airline, AirlineCreate, AirlineUpdate](Airline)
