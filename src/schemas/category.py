from pydantic import BaseModel
from pydantic import ConfigDict

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(CategoryBase):
    name: str
    description: str