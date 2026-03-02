from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Enum,
    DateTime,
    String,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class AttendanceStatus(str, enum.Enum):
    unknown = "unknown"
    present = "present"
    absent = "absent"


class TrainingParticipant(Base):
    __tablename__ = "training_participants"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        Integer,
        ForeignKey("training_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    attendance_status = Column(
        Enum(AttendanceStatus, name="attendance_status_enum",
        native_enum=False),
        nullable=False,
        default=AttendanceStatus.unknown,
        index=True,
    )

    certificate_number = Column(String(255), nullable=True)
    certificate_file_url = Column(String(1000), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    session = relationship("TrainingSession", back_populates="participants")
    employee = relationship("Employee")

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "employee_id",
            name="uq_session_employee"
        ),
        Index("ix_participant_session_attendance", "session_id", "attendance_status"),
    )