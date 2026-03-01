from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.repositories import application_repository


def get_all_applications(db: Session):
    return application_repository.get_applications(db)


def get_application_by_id(db: Session, application_id: int):
    application = application_repository.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


def create_application(db: Session, application_data: ApplicationCreate):
    application = Application(**application_data.model_dump())
    return application_repository.create_application(db, application)


def update_application(db: Session, application_id: int, data: ApplicationUpdate):
    application = application_repository.get_application(db, application_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(application, key, value)

    return application_repository.update_application(db, application)


def delete_application(db: Session, application_id: int):
    application = application_repository.get_application(db, application_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application_repository.delete_application(db, application)
    return {"message": "Application deleted"}