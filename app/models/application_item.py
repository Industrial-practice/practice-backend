from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from app.db.session import Base


class ApplicationItem(Base):
    __tablename__ = "application_items"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(Integer, ForeignKey("applications.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    session_id = Column(Integer, ForeignKey("training_sessions.id"), nullable=True)

    price_amount = Column(Numeric(14, 2))
    currency = Column(String)

    status = Column(String, default="pending")