from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    employee_id: Optional[int] = None
    is_active: Optional[bool] = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    employee_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    employee_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True