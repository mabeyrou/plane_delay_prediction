from schemas.flight import (
    FlightResponse,
    FlightCreate,
    FlightUpdate,
)
from routes.base_router import create_crud_router
from crud.flight import flight_crud

router = create_crud_router(
    crud_service=flight_crud,
    schema_create=FlightCreate,
    schema_read=FlightResponse,
    schema_update=FlightUpdate,
    prefix="/flights",
    tags=["flights"],
)
