from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class TrainingCourse(Base):
    __tablename__ = "training_courses"

    id = Column(Integer, primary_key=True)

    provider_id = Column(
        Integer,
        ForeignKey("providers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    title = Column(String(255), nullable=False, index=True)

    type = Column(String(100), nullable=True)

    description = Column(String(1000), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    provider = relationship("Provider", back_populates="courses")
    sessions = relationship(
        "TrainingSession",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_course_provider_active", "provider_id", "is_active"),
    )