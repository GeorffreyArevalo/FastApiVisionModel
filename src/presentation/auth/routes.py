
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data.database import SessionLocal
from src.data.schemas.user_schema import UserCreate, UserLogin, UserResponse
from src.infrastructure.datasource.user_datasource import UserDataSource


class AuthRoutes:
    
    @staticmethod
    def get_routes() -> APIRouter:
        router = APIRouter(
            prefix="/auth",
            tags=["auth"],
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
        
        @router.post("/create", response_model=UserResponse)
        async def create_user(user: UserCreate, db: Session = Depends(get_db)):
            return UserDataSource.create_user(db=db, user=user)
        
        @router.post("/login", response_model=UserResponse)
        async def login( user: UserLogin, db: Session = Depends(get_db) ):
            return UserDataSource.login(db=db, user=user)
        
        return router
        