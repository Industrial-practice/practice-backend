from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.training_session import (
    TrainingSessionCreate,
    TrainingSessionRead,
    TrainingSessionUpdate,
)
from app.services import training_session_service

router = APIRouter(prefix="/training-sessions", tags=["TrainingSessions"])


@router.get("/", response_model=list[TrainingSessionRead])
def get_training_sessions(db: Session = Depends(get_db)):
    return training_session_service.get_all_training_sessions(db)


@router.get("/{session_id}", response_model=TrainingSessionRead)
def get_training_session(session_id: int, db: Session = Depends(get_db)):
    session = training_session_service.get_training_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")
    return session


@router.post("/", response_model=TrainingSessionRead)
def create_training_session(session: TrainingSessionCreate, db: Session = Depends(get_db)):
    return training_session_service.create_training_session(db, session)


@router.put("/{session_id}", response_model=TrainingSessionRead)
def update_training_session(session_id: int, session: TrainingSessionUpdate, db: Session = Depends(get_db)):
    return training_session_service.update_training_session(db, session_id, session)


@router.delete("/{session_id}")
def delete_training_session(session_id: int, db: Session = Depends(get_db)):
    return training_session_service.delete_training_session(db, session_id)