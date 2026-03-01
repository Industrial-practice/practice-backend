from sqlalchemy.orm import Session
from app.models.application_item import ApplicationItem


def get_application_items(db: Session):
    return db.query(ApplicationItem).all()


def get_application_item(db: Session, item_id: int):
    return db.query(ApplicationItem).filter(ApplicationItem.id == item_id).first()


def create_application_item(db: Session, item: ApplicationItem):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_application_item(db: Session, item: ApplicationItem):
    db.commit()
    db.refresh(item)
    return item


def delete_application_item(db: Session, item: ApplicationItem):
    db.delete(item)
    db.commit()