from sqlalchemy.orm import Session
from app.models.org_unit import OrgUnit


def get_org_units(db: Session):
    return db.query(OrgUnit).all()


def get_org_unit(db: Session, org_unit_id: int):
    return db.query(OrgUnit).filter(OrgUnit.id == org_unit_id).first()


def create_org_unit(db: Session, org_unit: OrgUnit):
    db.add(org_unit)
    db.commit()
    db.refresh(org_unit)
    return org_unit


def update_org_unit(db: Session, org_unit: OrgUnit):
    db.commit()
    db.refresh(org_unit)
    return org_unit


def delete_org_unit(db: Session, org_unit: OrgUnit):
    db.delete(org_unit)
    db.commit()