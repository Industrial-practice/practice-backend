from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    employee_id: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    employee_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    employee_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    employee_id: Optional[int]
    is_active: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True