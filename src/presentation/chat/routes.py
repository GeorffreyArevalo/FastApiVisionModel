
from typing import Annotated, Optional

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from sqlalchemy.orm import Session

from src.data.database import SessionLocal
from src.infrastructure.datasource.chat_datasource import ChatDataSource
from src.infrastructure.datasource.user_datasource import UserDataSource
from src.utils.jwt_process import JwtUtil

from cloudinary.uploader import upload

class ChatRoutes:
    @staticmethod
    def get_routes() -> APIRouter:
        router = APIRouter(
            prefix="/chat",
            tags=["chat"],
            responses={
                400: {"message": "Bad Request"},
                404: {"message": "Not Found"}
            }
        )
        
        
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
                
        @router.post("/send_message")
        async def send_message(question: Annotated[str, Form()],
                             id_chat: Optional[int] = Form(None),
                             image: Optional[UploadFile] = File(None),
                             auth_username: str = Depends( JwtUtil.get_user_authenticated ),
                             db: Session = Depends(get_db)
            ):
            auth_user = UserDataSource.get_user_by_username(db=db, username=auth_username )
            
            if auth_user is None:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail='Acceso denegado.' )
            
            
            return ChatDataSource.send_message(db=db, image=image, question=question, id_chat=id_chat, id_user=auth_user.id)
        
        return router
        
        
    





