from pydantic import BaseModel



class EventBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    author_id: int


class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

    class Config:
        orm_mode = True

class EventUpdate(EventBase):
    name: str
    description: str