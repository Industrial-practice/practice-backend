from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TrainingCourseBase(BaseModel):
    provider_id: int
    title: str = Field(..., max_length=255)
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)


class TrainingCourseCreate(TrainingCourseBase):
    pass


class TrainingCourseUpdate(BaseModel):
    provider_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=255)
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class TrainingCourseRead(BaseModel):
    id: int

    provider_id: int
    title: str
    type: Optional[str]
    description: Optional[str]

    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True