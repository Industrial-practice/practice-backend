from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.training_participant import (
    TrainingParticipantCreate,
    TrainingParticipantRead,
    TrainingParticipantUpdate,
)
from app.services import training_participant_service

router = APIRouter(
    prefix="/training-participants",
    tags=["TrainingParticipants"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[TrainingParticipantRead])
def get_training_participants(db: Session = Depends(get_db)):
    return training_participant_service.get_all_participants(db)


@router.get("/{participant_id}", response_model=TrainingParticipantRead)
def get_training_participant(participant_id: int, db: Session = Depends(get_db)):
    participant = training_participant_service.get_participant_by_id(
        db, participant_id
    )
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@router.post("/", response_model=TrainingParticipantRead)
def create_training_participant(
    participant: TrainingParticipantCreate,
    db: Session = Depends(get_db),
):
    return training_participant_service.create_participant(db, participant)


@router.put("/{participant_id}", response_model=TrainingParticipantRead)
def update_training_participant(
    participant_id: int,
    participant: TrainingParticipantUpdate,
    db: Session = Depends(get_db),
):
    return training_participant_service.update_participant(
        db, participant_id, participant
    )


@router.delete("/{participant_id}")
def delete_training_participant(
    participant_id: int,
    db: Session = Depends(get_db),
):
    return training_participant_service.delete_participant(
        db, participant_id
    )