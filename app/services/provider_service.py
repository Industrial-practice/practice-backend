from sqlalchemy.orm import Session
from app.models.provider import Provider
from app.schemas.provider import ProviderCreate
from app.repositories import provider_repository
from fastapi import HTTPException


def get_all_providers(db: Session):
    return provider_repository.get_providers(db)


def get_provider_by_id(db: Session, provider_id: int):
    return provider_repository.get_provider(db, provider_id)


def create_provider(db: Session, provider_data: ProviderCreate):
    provider = Provider(**provider_data.model_dump())
    return provider_repository.create_provider(db, provider)

def update_provider(db: Session, provider_id: int, data):
    provider = provider_repository.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    for key, value in data.model_dump().items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider


def delete_provider(db: Session, provider_id: int):
    provider = provider_repository.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    return {"message": "Provider deleted"}