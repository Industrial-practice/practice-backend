from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.provider import ProviderCreate, ProviderUpdate, ProviderRead
from app.services import provider_service

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("/", response_model=list[ProviderRead])
def get_providers(db: Session = Depends(get_db)):
    return provider_service.get_all_providers(db)


@router.get("/{provider_id}", response_model=ProviderRead)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = provider_service.get_provider_by_id(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.post("/", response_model=ProviderRead)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    return provider_service.create_provider(db, provider)


@router.put("/{provider_id}", response_model=ProviderRead)
def update_provider(provider_id: int, provider: ProviderUpdate, db: Session = Depends(get_db)):
    return provider_service.update_provider(db, provider_id, provider)


@router.delete("/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    return provider_service.delete_provider(db, provider_id)