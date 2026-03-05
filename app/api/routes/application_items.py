from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.application_item import (
    ApplicationItemCreate,
    ApplicationItemRead,
    ApplicationItemUpdate,
)
from app.services import application_item_service

router = APIRouter(
    prefix="/application-items",
    tags=["ApplicationItems"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[ApplicationItemRead])
def get_application_items(db: Session = Depends(get_db)):
    return application_item_service.get_all_application_items(db)


@router.get("/{item_id}", response_model=ApplicationItemRead)
def get_application_item(item_id: int, db: Session = Depends(get_db)):
    item = application_item_service.get_application_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Application item not found")
    return item


@router.post("/", response_model=ApplicationItemRead)
def create_application_item(
    item: ApplicationItemCreate,
    db: Session = Depends(get_db)
):
    return application_item_service.create_application_item(db, item)


@router.put("/{item_id}", response_model=ApplicationItemRead)
def update_application_item(
    item_id: int,
    item: ApplicationItemUpdate,
    db: Session = Depends(get_db)
):
    return application_item_service.update_application_item(db, item_id, item)


@router.delete("/{item_id}")
def delete_application_item(item_id: int, db: Session = Depends(get_db)):
    return application_item_service.delete_application_item(db, item_id)