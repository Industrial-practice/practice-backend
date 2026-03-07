from sqlalchemy.orm import Session
from app.models.trainer import Trainer
from app.schemas.trainer import TrainerCreate, TrainerUpdate
from app.repositories import trainer_repository
from fastapi import HTTPException


def get_all_trainers(db: Session):
    return trainer_repository.get_trainers(db)


def get_trainer_by_id(db: Session, trainer_id: int):
    trainer = trainer_repository.get_trainer(db, trainer_id)

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    return trainer


def create_trainer(db: Session, trainer_data: TrainerCreate):
    trainer = Trainer(**trainer_data.model_dump())
    return trainer_repository.create_trainer(db, trainer)


def update_trainer(db: Session, trainer_id: int, data: TrainerUpdate):
    trainer = trainer_repository.get_trainer(db, trainer_id)

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(trainer, key, value)

    return trainer_repository.update_trainer(db, trainer)


def delete_trainer(db: Session, trainer_id: int):
    trainer = trainer_repository.get_trainer(db, trainer_id)

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    trainer_repository.delete_trainer(db, trainer)

    return {"message": "Trainer was deleted"}