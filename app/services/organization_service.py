from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.repositories import organization_repository


def get_all_organizations(db: Session):
    return organization_repository.get_organizations(db)


def get_organization_by_id(db: Session, organization_id: int):
    organization = organization_repository.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


def create_organization(db: Session, organization_data: OrganizationCreate):
    organization = Organization(**organization_data.model_dump())
    return organization_repository.create_organization(db, organization)


def update_organization(db: Session, organization_id: int, data: OrganizationUpdate):
    organization = organization_repository.get_organization(db, organization_id)

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(organization, key, value)

    return organization_repository.update_organization(db, organization)


def delete_organization(db: Session, organization_id: int):
    organization = organization_repository.get_organization(db, organization_id)

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    organization_repository.delete_organization(db, organization)
    return {"message": "Organization deleted"}