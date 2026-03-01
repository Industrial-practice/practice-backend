from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.repositories import role_repository


def get_all_roles(db: Session):
	return role_repository.get_roles(db)


def get_role_by_id(db: Session, role_id: int):
	role = role_repository.get_role(db, role_id)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")
	return role


def create_role(db: Session, role_data: RoleCreate):
	role = Role(**role_data.model_dump())
	return role_repository.create_role(db, role)


def update_role(db: Session, role_id: int, data: RoleUpdate):
	role = role_repository.get_role(db, role_id)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")

	for key, value in data.model_dump(exclude_unset=True).items():
		setattr(role, key, value)

	return role_repository.update_role(db, role)


def delete_role(db: Session, role_id: int):
	role = role_repository.get_role(db, role_id)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")

	role_repository.delete_role(db, role)
	return {"message": "Role deleted"}

