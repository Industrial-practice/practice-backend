from sqlalchemy.orm import Session
from app.models.trainer import Trainer
from app.schemas.trainer import TrainerCreate, TrainerUpdate
from app.repositories import trainer_repository
from fastapi import HTTPException


def get_all_trainers(db: Session):
    return trainer_repository.get_trainers(db)


def get_trainer_by_id(db: Session, trainer_id: int):
    course = trainer_repository.get_trainer_course(db, trainer_id)
    if not course:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return course


def create_trainer(db: Session, course_data: TrainerCreate):
    course = Trainer(**course_data.model_dump())
    return trainer_repository.create_trainer_course(db, course)

def update_trainer(db: Session, course_id: int, data: TrainerUpdate):
    course = trainer_repository.get_trainer_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Trainer not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    return trainer_repository.update_trainer_course(db, course)


def delete_trainer_course(db: Session, course_id: int):
    course = trainer_repository.get_trainer_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Trainer not found")

    trainer_repository.delete_trainer_course(db, course)
    return {"message": "Trainer was deleted"}