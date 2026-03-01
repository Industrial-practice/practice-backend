from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    name = Column(String)