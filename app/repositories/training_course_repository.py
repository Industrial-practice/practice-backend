from sqlalchemy.orm import Session
from app.models.training_course import TrainingCourse


def get_training_courses(db: Session):
    return db.query(TrainingCourse).all()


def get_training_course(db: Session, course_id: int):
    return db.query(TrainingCourse).filter(TrainingCourse.id == course_id).first()


def create_training_course(db: Session, course: TrainingCourse):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_training_course(db: Session, course: TrainingCourse):
    db.delete(course)
    db.commit()