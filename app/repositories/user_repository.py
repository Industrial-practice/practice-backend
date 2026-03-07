from sqlalchemy.orm import Session
from app.models.user import User


from sqlalchemy.orm import joinedload
from app.models.user_role import UserRole


def get_users(db: Session):
    return (
        db.query(User)
        .options(
            joinedload(User.user_roles)
            .joinedload(UserRole.role)
        )
        .all()
    )


def get_user(db: Session, user_id: int):
    return (
        db.query(User)
        .options(
            joinedload(User.user_roles)
            .joinedload(UserRole.role)
        )
        .filter(User.id == user_id)
        .first()
    )


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()