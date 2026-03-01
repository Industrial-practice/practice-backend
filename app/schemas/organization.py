from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str
    bin: Optional[str] = None
    address: Optional[str] = None
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    bin: Optional[str] = None
    address: Optional[str] = None
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class OrganizationRead(OrganizationBase):
    id: int
    is_active: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True