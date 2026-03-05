from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate
)
from app.services import application_service

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[ApplicationRead])
def get_applications(db: Session = Depends(get_db)):
    return application_service.get_all_applications(db)


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return application_service.get_application_by_id(db, application_id)


@router.post("/", response_model=ApplicationRead)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    return application_service.create_application(db, application)


@router.put("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    return application_service.update_application(db, application_id, application)


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    return application_service.delete_application(db, application_id)