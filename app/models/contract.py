from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from app.db.session import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))

    contract_number = Column(String, nullable=False)
    title = Column(String, nullable=True)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    currency = Column(String)
    budget_limit = Column(Numeric(14, 2))

    status = Column(String, default="draft")

    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())