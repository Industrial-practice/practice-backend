from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False, index=True)

    # БИН Казахстана - 12 символов
    bin = Column(String(12), nullable=False, unique=True, index=True)

    legal_address = Column(String(500), nullable=True)

    contacts_json = Column(JSONB, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    contracts = relationship("Contract", back_populates="provider")
    courses = relationship("TrainingCourse", back_populates="provider")
    trainers = relationship("Trainer", back_populates="provider")

    __table_args__ = (
        Index("ix_provider_active_name", "is_active", "name"),
    )