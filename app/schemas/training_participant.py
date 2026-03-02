from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AttendanceStatus(str, Enum):
    unknown = "unknown"
    present = "present"
    absent = "absent"


class TrainingParticipantBase(BaseModel):
    session_id: int
    employee_id: int


class TrainingParticipantCreate(TrainingParticipantBase):
    pass


class TrainingParticipantUpdate(BaseModel):
    session_id: Optional[int] = None
    employee_id: Optional[int] = None
    attendance_status: Optional[AttendanceStatus] = None

    certificate_number: Optional[str] = Field(None, max_length=255)
    certificate_file_url: Optional[str] = Field(None, max_length=1000)


class TrainingParticipantRead(BaseModel):
    id: int

    session_id: int
    employee_id: int

    attendance_status: AttendanceStatus

    certificate_number: Optional[str]
    certificate_file_url: Optional[str]

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True