from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Type, List
from database.engine import get_db
from crud.base import CRUDBase


def create_crud_router(
    *,
    crud_service: CRUDBase,
    schema_create: Type,
    schema_read: Type,
    schema_update: Type,
    prefix: str,
    tags: list = None,
):
    router = APIRouter(prefix=prefix, tags=tags or [prefix.strip("/")])

    @router.get("/", response_model=List[schema_read])
    def index(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
        return crud_service.get_multi(db, skip=skip, limit=limit)

    @router.get("/{item_id}", response_model=schema_read)
    def show(item_id: int, db: Session = Depends(get_db)):
        obj = crud_service.get(db, id=item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    @router.post("/", response_model=schema_read)
    def store(item: schema_create, db: Session = Depends(get_db)):
        obj = crud_service.create(db, obj_in=item)
        db.commit()
        return obj

    @router.put("/{item_id}", response_model=schema_read)
    def update(item_id: int, item: schema_update, db: Session = Depends(get_db)):
        db_obj = crud_service.get(db, id=item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not found")
        obj = crud_service.update(db, db_obj=db_obj, obj_in=item)
        db.commit()
        return obj

    @router.delete("/{item_id}")
    def destroy(item_id: int, db: Session = Depends(get_db)):
        obj = crud_service.remove(db, id=item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        db.commit()
        return {"ok": True, "detail": "Item deleted"}

    return router
