from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

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

    employee_number = Column(String(50), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)

    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)

    position = Column(String(255), nullable=True)
    grade = Column(String(100), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="employees")
    org_unit = relationship(
        "OrgUnit",
        back_populates="employees",
        foreign_keys=[org_unit_id]
    )
    user = relationship("User", back_populates="employee", uselist=False)

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "employee_number",
            name="uq_employee_number_per_org"
        ),
        Index("ix_employee_name", "last_name", "first_name"),
    )