from sqlalchemy.orm import Session
from app.models.training_participant import TrainingParticipant
from app.models.training_session import TrainingSession


def get_participants(db: Session):
    return db.query(TrainingParticipant).all()


def get_participant(db: Session, participant_id: int):
    return (
        db.query(TrainingParticipant)
        .filter(TrainingParticipant.id == participant_id)
        .first()
    )


def get_participants_by_session(db: Session, session_id: int):
    return (
        db.query(TrainingParticipant)
        .filter(TrainingParticipant.session_id == session_id)
        .all()
    )


def create_participant(db: Session, participant: TrainingParticipant):
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def update_participant(db: Session, participant: TrainingParticipant):
    db.commit()
    db.refresh(participant)
    return participant


def delete_participant(db: Session, participant: TrainingParticipant):
    db.delete(participant)
    db.commit()


def get_participants_by_course(db: Session, course_id: int):
    return (
        db.query(TrainingParticipant)
        .join(
            TrainingSession,
            TrainingParticipant.session_id == TrainingSession.id
        )
        .filter(TrainingSession.course_id == course_id)
        .all()
    )