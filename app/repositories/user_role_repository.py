from sqlalchemy.orm import Session
from app.models.user_role import UserRole


def get_user_roles(db: Session):
    return db.query(UserRole).all()


def get_roles_by_user(db: Session, user_id: int):
    return db.query(UserRole).filter(UserRole.user_id == user_id).all()


def get_users_by_role(db: Session, role_id: int):
    return db.query(UserRole).filter(UserRole.role_id == role_id).all()


def get_user_role(db: Session, user_id: int, role_id: int):
    return (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        )
        .first()
    )


def create_user_role(db: Session, user_role: UserRole):
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def delete_user_role(db: Session, user_role: UserRole):
    db.delete(user_role)
    db.commit()