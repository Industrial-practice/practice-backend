from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories import user_repository

from app.core.security import hash_password

def get_all_users(db: Session):
    return user_repository.get_users(db)


def get_user_by_id(db: Session, user_id: int):
    return user_repository.get_user(db, user_id)


def create_user(db: Session, user_data: UserCreate):
    data = user_data.model_dump()

    # достаем пароль
    password = data.pop("password")

    # хэшируем
    data["password_hash"] = hash_password(password)

    user = User(**data)
    return user_repository.create_user(db, user)


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = user_repository.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)

    # если обновляют пароль
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    return user_repository.update_user(db, user)


def delete_user(db: Session, user_id: int):
    user = user_repository.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_repository.delete_user(db, user)
    return {"message": "User deleted"}