from sqlalchemy.orm import Session
from app.models.application import Application


def get_applications(db: Session):
    return db.query(Application).all()


def get_application(db: Session, application_id: int):
    return db.query(Application).filter(Application.id == application_id).first()


def create_application(db: Session, application: Application):
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application(db: Session, application: Application):
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: Application):
    db.delete(application)
    db.commit()