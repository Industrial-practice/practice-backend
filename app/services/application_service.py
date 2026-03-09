from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models import ApplicationItem, TrainingParticipant
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationStatus, ApplicationStatus, ApplicationUpdate
from app.repositories import application_repository

from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

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


def approve_application(db: Session, application_id: int):
    application = get_application_by_id(db, application_id)

    if application.status != ApplicationStatus.pending:
        raise HTTPException(
            status_code=400,
            detail="Application cannot be approved"
        )

    if not application.contract_id:
        raise HTTPException(
            status_code=400,
            detail="Application has no contract"
        )

    contract = application.contract

    total_amount = db.query(
        func.coalesce(func.sum(ApplicationItem.price_amount), 0)
    ).filter(
        ApplicationItem.application_id == application_id
    ).scalar()

    for item in application.items:
        if item.currency != contract.currency:
            raise HTTPException(
                status_code=400,
                detail="Currency mismatch between item and contract"
            )

    if contract.budget_limit < total_amount:
        raise HTTPException(
            status_code=400,
            detail="Contract budget exceeded"
        )

    contract.budget_limit -= total_amount

    for item in application.items:

        item.status = "approved"

        if item.session_id:

            existing = db.query(TrainingParticipant).filter(
                TrainingParticipant.session_id == item.session_id,
                TrainingParticipant.employee_id == item.employee_id
            ).first()

            if not existing:
                participant = TrainingParticipant(
                    session_id=item.session_id,
                    employee_id=item.employee_id
                )

                db.add(participant)


    application.status = ApplicationStatus.approved
    application.approved_at = utc_now()

    db.commit()

    db.refresh(application)
    return application


def reject_application(db: Session, application_id: int):
    application = get_application_by_id(db, application_id)

    application.status = ApplicationStatus.rejected
    application.rejected_at = utc_now()

    db.commit()
    db.refresh(application)

    return application
