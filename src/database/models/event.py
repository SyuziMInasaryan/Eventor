
from sqlalchemy import Column, Integer, String, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from src.database.models.models import Base
from src.database.models.category import Category
from src.database.models.user import User


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    image = Column(LargeBinary)

    category_id = Column(Integer, ForeignKey("category.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="events")
    author = relationship("User", back_populates="events")