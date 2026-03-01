from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric
from app.db.session import Base


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("training_courses.id"))
    trainer_id = Column(Integer, nullable=True)

    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)

    city = Column(String)
    location = Column(String)

    price_amount = Column(Numeric(14, 2))
    currency = Column(String)

    status = Column(String, nullable=False, default="planned")