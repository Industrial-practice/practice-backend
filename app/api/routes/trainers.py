from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.trainer import (
    TrainerCreate,
    TrainerRead,
    TrainerUpdate
)
from app.services import trainer_service


router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[TrainerRead])
def get_trainers(db: Session = Depends(get_db)):
    return trainer_service.get_all_trainers(db)


@router.get("/{trainer_id}", response_model=TrainerRead)
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    return trainer_service.get_trainer_by_id(db, trainer_id)


@router.post("/", response_model=TrainerRead)
def create_trainer(
    trainer: TrainerCreate,
    db: Session = Depends(get_db)
):
    return trainer_service.create_trainer(db, trainer)


@router.put("/{trainer_id}", response_model=TrainerRead)
def update_trainer(
    trainer_id: int,
    trainer: TrainerUpdate,
    db: Session = Depends(get_db)
):
    return trainer_service.update_trainer(db, trainer_id, trainer)


@router.delete("/{trainer_id}")
def delete_trainer(trainer_id: int, db: Session = Depends(get_db)):
    return trainer_service.delete_trainer(db, trainer_id)