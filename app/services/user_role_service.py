from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate
from app.repositories import user_role_repository


def get_all_user_roles(db: Session):
    return user_role_repository.get_user_roles(db)


def get_roles_by_user(db: Session, user_id: int):
    return user_role_repository.get_roles_by_user(db, user_id)


def get_users_by_role(db: Session, role_id: int):
    return user_role_repository.get_users_by_role(db, role_id)


def assign_role_to_user(db: Session, data: UserRoleCreate):
    existing = user_role_repository.get_user_role(
        db, data.user_id, data.role_id
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already has this role",
        )

    user_role = UserRole(**data.model_dump())
    return user_role_repository.create_user_role(db, user_role)


def remove_role_from_user(db: Session, user_id: int, role_id: int):
    user_role = user_role_repository.get_user_role(db, user_id, role_id)

    if not user_role:
        raise HTTPException(
            status_code=404,
            detail="User role not found",
        )

    user_role_repository.delete_user_role(db, user_role)
    return {"message": "Role removed from user"}