from schemas.airline import (
    AirlineResponse,
    AirlineCreate,
    AirlineUpdate,
)
from routes.base_router import create_crud_router
from crud.airline import airline_crud

router = create_crud_router(
    crud_service=airline_crud,
    schema_create=AirlineCreate,
    schema_read=AirlineResponse,
    schema_update=AirlineUpdate,
    prefix="/airlines",
    tags=["airlines"],
)
