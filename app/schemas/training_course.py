from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrainingCourseBase(BaseModel):
    provider_id: int
    title: str
    type: Optional[str] = None
    description: Optional[str] = None


class TrainingCourseCreate(TrainingCourseBase):
    pass


class TrainingCourseUpdate(BaseModel):
    provider_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TrainingCourseRead(TrainingCourseBase):
    id: int
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True