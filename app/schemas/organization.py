from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    bin: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Organization name cannot be empty")
        return v.strip()

    @field_validator("bin")
    @classmethod
    def bin_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v.isdigit() or len(v) != 12:
            raise ValueError("BIN must be exactly 12 digits")
        return v


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    bin: Optional[str] = Field(None, max_length=12)
    address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("bin")
    @classmethod
    def bin_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v.isdigit() or len(v) != 12:
            raise ValueError("BIN must be exactly 12 digits")
        return v

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