from sqlalchemy import Column, ForeignKey, Integer, String

from src.data.database import Base


class ChatModel(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    image = Column(String, nullable=True)
    vectorial_db_id = Column(String, nullable=True)
    user_id = Column( Integer,  ForeignKey("users.id"))

