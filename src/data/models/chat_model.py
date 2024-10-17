from sqlalchemy import Column, ForeignKey, Integer, String

from src.data.database import Base


class ChatModel(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    user_id = Column( Integer,  ForeignKey("users.id"))

