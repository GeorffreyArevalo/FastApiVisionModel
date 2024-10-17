from pydantic import BaseModel


class ChatCreate(BaseModel):
    title: str | None

class ChatSchema(ChatCreate):
    id: int
    user_id: str
    class Config:
        orm_mode = True

