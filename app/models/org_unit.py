from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class OrgUnit(Base):
    __tablename__ = "org_units"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    parent_id = Column(Integer, ForeignKey("org_units.id"), nullable=True)

    name = Column(String, nullable=False)
    code = Column(String, nullable=True)

    manager_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())