from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)

    provider_id = Column(
        Integer,
        ForeignKey("providers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    full_name = Column(String(255), nullable=False)

    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=True)

    bio = Column(String, nullable=True)

    certifications_json = Column(JSONB, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    provider = relationship("Provider", back_populates="trainers")

    __table_args__ = (
        Index("idx_trainers_full_name", "full_name"),
    )