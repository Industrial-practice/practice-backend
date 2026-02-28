from pydantic import BaseModel
from typing import Optional


class TrainingParticipantBase(BaseModel):
    session_id: int
    employee_id: int


class TrainingParticipantCreate(TrainingParticipantBase):
    pass


class TrainingParticipantUpdate(BaseModel):
    session_id: Optional[int] = None
    employee_id: Optional[int] = None
    attendance_status: Optional[str] = None


class TrainingParticipantRead(TrainingParticipantBase):
    id: int
    attendance_status: str

    class Config:
        from_attributes = True