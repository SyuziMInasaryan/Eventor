
from sqlalchemy import Column, Integer, String, Text,  ForeignKey
from sqlalchemy.orm import relationship

from src.database.models.models import Base



class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    image_path = Column(String(512), nullable=True)

    category_id = Column(Integer, ForeignKey("category.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="events")
    author = relationship("User", back_populates="events")

