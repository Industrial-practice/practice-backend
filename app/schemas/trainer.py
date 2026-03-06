from pydantic import BaseModel, EmailStr
from typing import Any, Optional, List, Dict
from datetime import datetime


class TrainerBase(BaseModel):
    provider_id: Optional[int] = None
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    certifications_json: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = True


class TrainerCreate(TrainerBase):
    pass


class TrainerUpdate(BaseModel):
    provider_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    certifications_json: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TrainerRead(TrainerBase):
    id: int
    full_name: str
    email: Optional[EmailStr] = None   
    phone: Optional[str] = None
    bio: Optional[str] = None
    contacts_json: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

        
class TrainerList(BaseModel):
    items: List[TrainerRead]
    total: int
