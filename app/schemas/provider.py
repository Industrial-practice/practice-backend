from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime


class ProviderBase(BaseModel):
    name: str = Field(..., max_length=255)
    bin: str = Field(..., max_length=12)
    legal_address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Provider name cannot be empty")
        return v.strip()

    @field_validator("bin")
    @classmethod
    def bin_format(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit() or len(v) != 12:
            raise ValueError("BIN must be exactly 12 digits")
        return v



class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    legal_address: Optional[str] = Field(None, max_length=500)
    contacts_json: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Provider name cannot be empty")
        return v.strip()


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