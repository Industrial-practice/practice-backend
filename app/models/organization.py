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


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)

    parent_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name = Column(String(255), nullable=False, index=True)

    bin = Column(String(12), nullable=True, unique=True)

    address = Column(String(500), nullable=True)
    contacts_json = Column(JSONB, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Self hierarchy
    parent = relationship("Organization", remote_side=[id], backref="children")

    # Relationships

    contracts = relationship(
        "Contract",
        back_populates="organization",
        passive_deletes=True
    )
    employees = relationship(
        "Employee",
        back_populates="organization",
        passive_deletes=True
    )

    org_units = relationship(
        "OrgUnit",
        back_populates="organization",
        passive_deletes=True
    )

    applications = relationship(
        "Application",
        back_populates="organization",
        passive_deletes=True
    )

    __table_args__ = (
        Index("ix_org_active_name", "is_active", "name"),
    )