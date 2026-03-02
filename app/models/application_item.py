from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    String,
    Enum,
    UniqueConstraint, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class ApplicationItemStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApplicationItem(Base):
    __tablename__ = "application_items"

    id = Column(Integer, primary_key=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey("training_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    price_amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(10), nullable=False)

    status = Column(
        Enum(ApplicationItemStatus, name="application_item_status_enum",
        native_enum=False),
        nullable=False,
        default=ApplicationItemStatus.pending,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    application = relationship("Application", back_populates="items")
    employee = relationship("Employee")
    session = relationship("TrainingSession")

    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "employee_id",
            name="uq_application_employee"
        ),
    )