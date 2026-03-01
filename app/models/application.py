from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from app.db.session import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    requested_by_user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    org_unit_id = Column(Integer, ForeignKey("org_units.id"))

    course_id = Column(Integer, ForeignKey("training_courses.id"))

    status = Column(String, nullable=False, default="pending")

    comment = Column(String, nullable=True)

    submitted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())