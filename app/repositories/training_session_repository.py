from sqlalchemy.orm import Session
from app.models.training_session import TrainingSession


def get_training_sessions(db: Session):
    return db.query(TrainingSession).all()


def get_training_session(db: Session, session_id: int):
    return db.query(TrainingSession).filter(TrainingSession.id == session_id).first()


def create_training_session(db: Session, session: TrainingSession):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def update_training_session(db: Session, session: TrainingSession):
    db.commit()
    db.refresh(session)
    return session

def delete_training_session(db: Session, session: TrainingSession):
    db.delete(session)
    db.commit()