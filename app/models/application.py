from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String,
    Enum,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    requested_by_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    org_unit_id = Column(
        Integer,
        ForeignKey("org_units.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    contract_id = Column(
        Integer,
        ForeignKey("contracts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    course_id = Column(
        Integer,
        ForeignKey("training_courses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status = Column(
        Enum(ApplicationStatus, name="application_status_enum",
        native_enum=False),
        nullable=False,
        default=ApplicationStatus.pending,
        index=True,
    )

    comment = Column(String, nullable=True)

    submitted_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    requested_by_user = relationship("User")
    organization = relationship("Organization", back_populates="applications")
    org_unit = relationship("OrgUnit")
    contract = relationship("Contract", back_populates="applications")
    course = relationship("TrainingCourse")
    items = relationship(
        "ApplicationItem",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_applications_status_org", "status", "organization_id"),
    )