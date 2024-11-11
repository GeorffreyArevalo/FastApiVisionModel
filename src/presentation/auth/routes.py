
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.data.database import SessionLocal
from src.data.schemas.user_schema import UserCreate, UserLogin, UserResponse
from src.infrastructure.datasource.user_datasource import UserDataSource

from src.utils.jwt_process import JwtUtil



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
        
        @router.get("/renew")
        async def check_token(
            auth_username: str = Depends( JwtUtil.get_user_authenticated ),
            db: Session = Depends(get_db)
        ):
            auth_user = UserDataSource.get_user_by_username(db=db, username=auth_username )
            
            if auth_user is None:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail='Acceso denegado.' )
            
            token = UserDataSource.check_token(db=db, username=auth_user.username)
            
            return {
                "user": auth_user,
                "token": token
            }
            
        return router
        