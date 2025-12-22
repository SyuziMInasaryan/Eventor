from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.models.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    events = relationship("Event", back_populates="author")
