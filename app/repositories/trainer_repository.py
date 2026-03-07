from sqlalchemy.orm import Session
from app.models.trainer import Trainer


def get_trainers(db: Session):
    return db.query(Trainer).all()


def get_trainer(db: Session, trainer_id: int):
    return db.query(Trainer).filter(Trainer.id == trainer_id).first()


def create_trainer(db: Session, trainer: Trainer):
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    return trainer


def update_trainer(db: Session, trainer: Trainer):
    db.commit()
    db.refresh(trainer)
    return trainer


def delete_trainer(db: Session, trainer: Trainer):
    db.delete(trainer)
    db.commit()