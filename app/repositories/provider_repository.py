from sqlalchemy.orm import Session
from app.models.provider import Provider


def get_providers(db: Session):
    return db.query(Provider).all()


def get_provider(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()


def create_provider(db: Session, provider: Provider):
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider

def update_provider(db: Session, provider: Provider):
    db.commit()
    db.refresh(provider)
    return provider

def delete_provider(db: Session, provider: Provider):
    db.delete(provider)
    db.commit()