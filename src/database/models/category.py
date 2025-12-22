
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.models.models import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    events = relationship("Event", back_populates="category")
