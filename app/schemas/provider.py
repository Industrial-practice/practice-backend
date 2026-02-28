from pydantic import BaseModel
from typing import Optional


class ProviderBase(BaseModel):
    name: str
    bin: str
    legal_address: Optional[str] = None
    contacts_json: Optional[str] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: Optional[str]
    legal_address: Optional[str]
    contacts_json: Optional[str]
    is_active: Optional[bool]

class ProviderRead(ProviderBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True