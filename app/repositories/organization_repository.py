from sqlalchemy.orm import Session
from app.models.organization import Organization


def get_organizations(db: Session):
    return db.query(Organization).all()


def get_organization(db: Session, organization_id: int):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def create_organization(db: Session, organization: Organization):
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def update_organization(db: Session, organization: Organization):
    db.commit()
    db.refresh(organization)
    return organization


def delete_organization(db: Session, organization: Organization):
    db.delete(organization)
    db.commit()