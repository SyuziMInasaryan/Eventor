from pydantic import BaseModel
from pydantic import ConfigDict


class EventBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    author_id: int


class EventCreate(EventBase):
    pass



class EventRead(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EventUpdate(EventBase):
    name: str
    description: str
