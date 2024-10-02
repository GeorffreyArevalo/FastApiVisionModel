from pydantic import BaseModel


class ChatCreate(BaseModel):
    question: str

class ChatBase(ChatCreate):
    answer: str

class ChatSchema(ChatBase):
    id: int
    image: str | None
    vectorial_db_id: str | None
    user_id: str
    class Config:
        orm_mode = True

