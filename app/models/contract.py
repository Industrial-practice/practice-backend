from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    Index,
    UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class ContractStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    suspended = "suspended"
    closed = "closed"
    expired = "expired"


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)

    provider_id = Column(
        Integer,
        ForeignKey("providers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    contract_number = Column(String(100), nullable=False)
    title = Column(String(255), nullable=True)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    currency = Column(String(10), nullable=False)
    budget_limit = Column(Numeric(14, 2), nullable=False)

    status = Column(
        Enum(ContractStatus, name="contract_status_enum",
        native_enum=False),
        nullable=False,
        default=ContractStatus.draft,
        index=True,
    )

    created_by_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    provider = relationship("Provider", back_populates="contracts")
    created_by_user = relationship("User")
    applications = relationship("Application", back_populates="contract")

    __table_args__ = (
        UniqueConstraint(
            "provider_id",
            "contract_number",
            name="uq_provider_contract_number"
        ),
        CheckConstraint("end_date > start_date", name="chk_contract_dates"),
        Index("ix_contract_status_provider", "status", "provider_id"),
    )