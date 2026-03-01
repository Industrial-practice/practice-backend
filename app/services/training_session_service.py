from sqlalchemy.orm import Session
from app.models.training_session import TrainingSession
from app.schemas.training_session import TrainingSessionCreate
from app.repositories import training_session_repository
from fastapi import HTTPException


def get_all_training_sessions(db: Session):
    return training_session_repository.get_training_sessions(db)


def get_training_session_by_id(db: Session, session_id: int):
    return training_session_repository.get_training_session(db, session_id)


def create_training_session(db: Session, session_data: TrainingSessionCreate):
    session = TrainingSession(**session_data.model_dump())
    return training_session_repository.create_training_session(db, session)

def update_training_session(db: Session, session_id: int, data):
    session = training_session_repository.get_training_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    for key, value in data.model_dump().items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


def delete_training_session(db: Session, session_id: int):
    session = training_session_repository.get_training_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    db.delete(session)
    db.commit()
    return {"message": "Training session deleted"}