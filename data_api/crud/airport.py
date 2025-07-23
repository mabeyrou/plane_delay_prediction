from crud.base import CRUDBase
from models.airport import Airport
from schemas.airport import AirportCreate, AirportUpdate


airport_crud = CRUDBase[Airport, AirportCreate, AirportUpdate](Airport)
