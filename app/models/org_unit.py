from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class OrgUnit(Base):
    __tablename__ = "org_units"

    id = Column(Integer, primary_key=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parent_id = Column(
        Integer,
        ForeignKey("org_units.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)

    manager_employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="SET NULL", use_alter=True),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="org_units")

    parent = relationship("OrgUnit", remote_side=[id], backref="children")

    manager = relationship(
        "Employee",
        foreign_keys=[manager_employee_id]
    )
    employees = relationship(
        "Employee",
        back_populates="org_unit",
        foreign_keys="Employee.org_unit_id"
    )
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "code",
            name="uq_orgunit_code_per_org"
        ),
        Index("ix_orgunit_org_parent", "organization_id", "parent_id"),
    )