from schemas.airport import (
    AirportResponse,
    AirportCreate,
    AirportUpdate,
)
from routes.base_router import create_crud_router
from crud.airport import airport_crud

router = create_crud_router(
    crud_service=airport_crud,
    schema_create=AirportCreate,
    schema_read=AirportResponse,
    schema_update=AirportUpdate,
    prefix="/airports",
    tags=["airports"],
)
