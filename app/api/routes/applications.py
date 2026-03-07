from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_org_unit_id,
    get_current_organization_id,
    get_current_user,
    get_scoped_application,
    is_employee,
    is_head,
    is_hr,
)
from app.db.session import get_db
from app.models.application import Application
from app.models.user import User
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
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if is_hr(current_user):
        return application_service.get_all_applications(db)

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        if current_org_unit_id is None:
            return []
        return (
            db.query(Application)
            .filter(Application.org_unit_id == current_org_unit_id)
            .all()
        )

    if is_employee(current_user):
        return (
            db.query(Application)
            .filter(Application.requested_by_user_id == current_user.id)
            .all()
        )

    return []


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    target_application: Application = Depends(get_scoped_application),
):
    return target_application


@router.post("/", response_model=ApplicationRead)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if is_hr(current_user):
        return application_service.create_application(db, application)

    if is_head(current_user):
        current_org_id = get_current_organization_id(current_user)
        current_org_unit_id = get_current_org_unit_id(current_user)

        if current_org_id is None or current_org_unit_id is None:
            raise HTTPException(status_code=403, detail="Forbidden")

        if application.organization_id != current_org_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        if application.org_unit_id != current_org_unit_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return application_service.create_application(db, application)

    raise HTTPException(status_code=403, detail="Forbidden")


@router.put("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_application: Application = Depends(get_scoped_application),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return application_service.update_application(db, application_id, application)


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_application: Application = Depends(get_scoped_application),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return application_service.delete_application(db, application_id)


@router.post("/{application_id}/approve", response_model=ApplicationRead)
def approve_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_application: Application = Depends(get_scoped_application),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return application_service.approve_application(db, application_id)


@router.post("/{application_id}/reject", response_model=ApplicationRead)
def reject_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_application: Application = Depends(get_scoped_application),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return application_service.reject_application(db, application_id)