from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate
)
from app.services import organization_service

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/", response_model=list[OrganizationRead])
def get_organizations(db: Session = Depends(get_db)):
    return organization_service.get_all_organizations(db)


@router.get("/{organization_id}", response_model=OrganizationRead)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    return organization_service.get_organization_by_id(db, organization_id)


@router.post("/", response_model=OrganizationRead)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db)
):
    return organization_service.create_organization(db, organization)


@router.put("/{organization_id}", response_model=OrganizationRead)
def update_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    return organization_service.update_organization(db, organization_id, organization)


@router.delete("/{organization_id}")
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    return organization_service.delete_organization(db, organization_id)