from sqlalchemy.orm import Session
from app.models.provider import Provider
from app.schemas.provider import ProviderCreate, ProviderUpdate
from app.repositories import provider_repository
from fastapi import HTTPException


def get_all_providers(db: Session):
    return provider_repository.get_providers(db)


def get_provider_by_id(db: Session, provider_id: int):
    provider = provider_repository.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

def create_provider(db: Session, provider_data: ProviderCreate):
    provider = Provider(**provider_data.model_dump())
    return provider_repository.create_provider(db, provider)

def update_provider(db: Session, provider_id: int, data: ProviderUpdate):
    provider = provider_repository.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # exclude_unset=True — обновляем только то, что реально передали
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)

    return provider_repository.update_provider(db, provider)


def delete_provider(db: Session, provider_id: int):
    provider = provider_repository.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    provider_repository.delete_provider(db, provider)
    return {"message": "Provider deleted"}