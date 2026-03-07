from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.training_participant import TrainingParticipant
from app.schemas.training_participant import (
    TrainingParticipantCreate,
    TrainingParticipantUpdate,
)
from app.repositories import training_participant_repository


def get_all_participants(db: Session):
    return training_participant_repository.get_participants(db)


def get_participant_by_id(db: Session, participant_id: int):
    participant = training_participant_repository.get_participant(
        db, participant_id
    )
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


def get_participants_by_session(db: Session, session_id: int):
    return training_participant_repository.get_participants_by_session(
        db, session_id
    )


def create_participant(db: Session, data: TrainingParticipantCreate):
    participant = TrainingParticipant(**data.model_dump())
    return training_participant_repository.create_participant(db, participant)


def update_participant(
    db: Session, participant_id: int, data: TrainingParticipantUpdate
):
    participant = training_participant_repository.get_participant(
        db, participant_id
    )

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(participant, key, value)

    return training_participant_repository.update_participant(db, participant)


def delete_participant(db: Session, participant_id: int):
    participant = training_participant_repository.get_participant(
        db, participant_id
    )

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    training_participant_repository.delete_participant(db, participant)
    return {"message": "Participant deleted"}

from app.repositories import training_participant_repository


def get_participants_by_course(db: Session, course_id: int):
    return training_participant_repository.get_participants_by_course(db, course_id)