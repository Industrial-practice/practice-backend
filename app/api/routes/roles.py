from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services import role_service

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[RoleRead])
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_all_roles(db)


@router.get("/{role_id}", response_model=RoleRead)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RoleRead)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_service.create_role(db, role)


@router.put("/{role_id}", response_model=RoleRead)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return role_service.update_role(db, role_id, role)


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return role_service.delete_role(db, role_id)