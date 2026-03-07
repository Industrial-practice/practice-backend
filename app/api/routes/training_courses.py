from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.training_course import TrainingCourseCreate, TrainingCourseRead, TrainingCourseUpdate
from app.services import training_course_service
from app.services import training_participant_service
from app.schemas.training_participant import TrainingParticipantRead

router = APIRouter(
    prefix="/training-courses",
    tags=["TrainingCourses"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[TrainingCourseRead])
def get_training_courses(db: Session = Depends(get_db)):
    return training_course_service.get_all_training_courses(db)


@router.get("/{course_id}", response_model=TrainingCourseRead)
def get_training_course(course_id: int, db: Session = Depends(get_db)):
    course = training_course_service.get_training_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Training course not found")
    return course


@router.post("/", response_model=TrainingCourseRead)
def create_training_course(course: TrainingCourseCreate, db: Session = Depends(get_db)):
    return training_course_service.create_training_course(db, course)


@router.put("/{course_id}", response_model=TrainingCourseRead)
def update_training_course(course_id: int, course: TrainingCourseUpdate, db: Session = Depends(get_db)):
    return training_course_service.update_training_course(db, course_id, course)


@router.delete("/{course_id}")
def delete_training_course(course_id: int, db: Session = Depends(get_db)):
    return training_course_service.delete_training_course(db, course_id)


@router.get("/{course_id}/participants", response_model=list[TrainingParticipantRead])
def get_course_participants(
    course_id: int,
    db: Session = Depends(get_db)
):
    return training_participant_service.get_participants_by_course(db, course_id)