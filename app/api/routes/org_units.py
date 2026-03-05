from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.org_unit import (
    OrgUnitCreate,
    OrgUnitRead,
    OrgUnitUpdate,
)
from app.services import org_unit_service

router = APIRouter(
    prefix="/org-units",
    tags=["OrgUnits"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[OrgUnitRead])
def get_org_units(db: Session = Depends(get_db)):
    return org_unit_service.get_all_org_units(db)


@router.get("/{org_unit_id}", response_model=OrgUnitRead)
def get_org_unit(org_unit_id: int, db: Session = Depends(get_db)):
    org_unit = org_unit_service.get_org_unit_by_id(db, org_unit_id)
    if not org_unit:
        raise HTTPException(status_code=404, detail="Org unit not found")
    return org_unit


@router.post("/", response_model=OrgUnitRead)
def create_org_unit(
    org_unit: OrgUnitCreate,
    db: Session = Depends(get_db)
):
    return org_unit_service.create_org_unit(db, org_unit)


@router.put("/{org_unit_id}", response_model=OrgUnitRead)
def update_org_unit(
    org_unit_id: int,
    org_unit: OrgUnitUpdate,
    db: Session = Depends(get_db)
):
    return org_unit_service.update_org_unit(db, org_unit_id, org_unit)


@router.delete("/{org_unit_id}")
def delete_org_unit(org_unit_id: int, db: Session = Depends(get_db)):
    return org_unit_service.delete_org_unit(db, org_unit_id)