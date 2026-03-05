from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.user_role import UserRoleCreate, UserRoleRead
from app.services import user_role_service

router = APIRouter(
    prefix="/user-roles",
    tags=["UserRoles"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[UserRoleRead])
def get_user_roles(db: Session = Depends(get_db)):
    return user_role_service.get_all_user_roles(db)


@router.get("/user/{user_id}", response_model=list[UserRoleRead])
def get_roles_by_user(user_id: int, db: Session = Depends(get_db)):
    return user_role_service.get_roles_by_user(db, user_id)


@router.get("/role/{role_id}", response_model=list[UserRoleRead])
def get_users_by_role(role_id: int, db: Session = Depends(get_db)):
    return user_role_service.get_users_by_role(db, role_id)


@router.post("/", response_model=UserRoleRead)
def assign_role_to_user(
    user_role: UserRoleCreate,
    db: Session = Depends(get_db),
):
    return user_role_service.assign_role_to_user(db, user_role)


@router.delete("/{user_id}/{role_id}")
def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
):
    return user_role_service.remove_role_from_user(
        db, user_id, role_id
    )