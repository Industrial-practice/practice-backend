from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.session import Base


class TrainingParticipant(Base):
    __tablename__ = "training_participants"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("training_sessions.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))

    attendance_status = Column(String, default="unknown")