from sqlalchemy.orm import Session
from app.models.training_session import TrainingSession
from app.schemas.training_session import TrainingSessionCreate, TrainingSessionUpdate
from app.repositories import training_session_repository
from fastapi import HTTPException


def get_all_training_sessions(db: Session):
    return training_session_repository.get_training_sessions(db)


def get_training_session_by_id(db: Session, session_id: int):
    session = training_session_repository.get_training_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")
    return session


def create_training_session(db: Session, session_data: TrainingSessionCreate):
    session = TrainingSession(**session_data.model_dump())
    return training_session_repository.create_training_session(db, session)

def update_training_session(db: Session, session_id: int, data: TrainingSessionUpdate):
    session = training_session_repository.get_training_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(session, key, value)

    return training_session_repository.update_training_session(db, session)


def delete_training_session(db: Session, session_id: int):
    session = training_session_repository.get_training_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    training_session_repository.delete_training_session(db, session)
    return {"message": "Training session deleted"}