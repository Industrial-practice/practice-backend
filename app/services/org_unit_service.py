from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.org_unit import OrgUnit
from app.schemas.org_unit import OrgUnitCreate, OrgUnitUpdate
from app.repositories import org_unit_repository


def get_all_org_units(db: Session):
    return org_unit_repository.get_org_units(db)


def get_org_unit_by_id(db: Session, org_unit_id: int):
    org_unit = org_unit_repository.get_org_unit(db, org_unit_id)
    if not org_unit:
        raise HTTPException(status_code=404, detail="Org unit not found")
    return org_unit


def create_org_unit(db: Session, org_unit_data: OrgUnitCreate):
    org_unit = OrgUnit(**org_unit_data.model_dump())
    return org_unit_repository.create_org_unit(db, org_unit)


def update_org_unit(db: Session, org_unit_id: int, data: OrgUnitUpdate):
    org_unit = org_unit_repository.get_org_unit(db, org_unit_id)

    if not org_unit:
        raise HTTPException(status_code=404, detail="Org unit not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(org_unit, key, value)

    return org_unit_repository.update_org_unit(db, org_unit)


def delete_org_unit(db: Session, org_unit_id: int):
    org_unit = org_unit_repository.get_org_unit(db, org_unit_id)

    if not org_unit:
        raise HTTPException(status_code=404, detail="Org unit not found")

    org_unit_repository.delete_org_unit(db, org_unit)
    return {"message": "Org unit deleted"}