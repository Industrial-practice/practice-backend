from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
    Numeric,
    Enum,
    Boolean,
    CheckConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class SessionStatus(str, enum.Enum):
    planned = "planned"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class SessionType(str, enum.Enum):
    seminar = "seminar"
    training = "training"
    certification = "certification"


class PricingType(str, enum.Enum):
    per_person = "per_person"
    per_group = "per_group"


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True)

    course_id = Column(
        Integer,
        ForeignKey("training_courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    trainer_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True,
    )

    session_type = Column(
        Enum(SessionType, name="session_type_enum", native_enum=False),
        nullable=False,
    )

    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    city = Column(String(255), nullable=True)
    location = Column(String(500), nullable=True)

    pricing_type = Column(
        Enum(PricingType, name="pricing_type_enum", native_enum=False),
        nullable=False,
        default=PricingType.per_person,
    )

    price_amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(10), nullable=False)

    status = Column(
        Enum(SessionStatus, name="session_status_enum",
        native_enum=False),
        nullable=False,
        default=SessionStatus.planned,
        index=True,
    )

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    course = relationship("TrainingCourse", back_populates="sessions")
    trainer = relationship("Employee")
    participants = relationship(
        "TrainingParticipant",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("end_datetime > start_datetime", name="chk_session_dates"),
        Index("ix_session_course_status", "course_id", "status"),
    )
