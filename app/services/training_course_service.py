from sqlalchemy.orm import Session
from app.models.training_course import TrainingCourse
from app.schemas.training_course import TrainingCourseCreate
from app.repositories import training_course_repository
from fastapi import HTTPException


def get_all_training_courses(db: Session):
    return training_course_repository.get_training_courses(db)


def get_training_course_by_id(db: Session, course_id: int):
    return training_course_repository.get_training_course(db, course_id)


def create_training_course(db: Session, course_data: TrainingCourseCreate):
    course = TrainingCourse(**course_data.model_dump())
    return training_course_repository.create_training_course(db, course)

def update_training_course(db: Session, course_id: int, data):
    course = training_course_repository.get_training_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Training course not found")

    for key, value in data.model_dump().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


def delete_training_course(db: Session, course_id: int):
    course = training_course_repository.get_training_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Training course not found")

    db.delete(course)
    db.commit()
    return {"message": "Training course deleted"}