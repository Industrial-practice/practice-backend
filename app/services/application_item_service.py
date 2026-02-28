from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.application_item import ApplicationItem
from app.schemas.application_item import ApplicationItemCreate, ApplicationItemUpdate
from app.repositories import application_item_repository


def get_all_application_items(db: Session):
    return application_item_repository.get_application_items(db)


def get_application_item_by_id(db: Session, item_id: int):
    item = application_item_repository.get_application_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Application item not found")
    return item


def create_application_item(db: Session, item_data: ApplicationItemCreate):
    item = ApplicationItem(**item_data.model_dump())
    return application_item_repository.create_application_item(db, item)


def update_application_item(db: Session, item_id: int, data: ApplicationItemUpdate):
    item = application_item_repository.get_application_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Application item not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    return application_item_repository.update_application_item(db, item)


def delete_application_item(db: Session, item_id: int):
    item = application_item_repository.get_application_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Application item not found")

    application_item_repository.delete_application_item(db, item)
    return {"message": "Application item deleted"}