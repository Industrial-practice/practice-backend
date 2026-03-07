from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_org_unit_id,
    get_current_user,
    get_scoped_user,
    is_employee,
    is_head,
    is_hr,
)
from app.db.session import get_db
from app.models.employee import Employee
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate
)
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[UserRead])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if is_hr(current_user):
        return user_service.get_all_users(db)

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        if current_org_unit_id is None:
            return []
        return (
            db.query(User)
            .join(Employee, User.employee_id == Employee.id)
            .filter(Employee.org_unit_id == current_org_unit_id)
            .all()
        )

    if is_employee(current_user):
        return [current_user]

    return []


@router.get("/{user_id}", response_model=UserRead)
def get_user(target_user: User = Depends(get_scoped_user)):
    return target_user





@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_user: User = Depends(get_scoped_user),
):
    if not is_hr(current_user):
        if is_head(current_user) and target_user.id == current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        if is_employee(current_user) and target_user.id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    return user_service.update_user(db, user_id, user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return user_service.delete_user(db, user_id)