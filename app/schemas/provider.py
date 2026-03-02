from pydantic import BaseModel, Field, constr
from typing import Optional, Dict, Any
from datetime import datetime


class ProviderBase(BaseModel):
    name: str = Field(..., max_length=255)

    bin: str = Field(..., max_length=12)

    legal_address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    legal_address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ProviderRead(BaseModel):
    id: int

    name: str
    bin: str
    legal_address: Optional[str]
    contacts_json: Optional[Dict[str, Any]]

    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True