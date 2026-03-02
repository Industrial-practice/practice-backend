from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    bin: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    bin: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class OrganizationRead(BaseModel):
    id: int

    name: str
    bin: Optional[str]
    address: Optional[str]
    contacts_json: Optional[Dict[str, Any]]
    parent_id: Optional[int]

    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True