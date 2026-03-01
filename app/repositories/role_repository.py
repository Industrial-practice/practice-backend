from sqlalchemy.orm import Session
from app.models.role import Role


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role: Role):
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role):
    db.delete(role)
    db.commit()