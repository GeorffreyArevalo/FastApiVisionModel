
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.data.models.user_model import UserModel
from src.data.schemas.user_schema import UserCreate, UserLogin
from src.utils.hash_password import HashPassword
from src.utils.jwt_process import JwtUtil

hash_utils = HashPassword()

class UserDataSource:
        
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        
        user_saved = UserDataSource.get_user_by_username(db=db, username=user.username)
        if user_saved:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El nombre de usuario ya existe.')
        
        password = user.password
        hashed_password = hash_utils.get_password_hash(password=password)
        db_user = UserModel( name=user.name, username=user.username, password=hashed_password )
        db.add( db_user )
        db.commit()
        db.refresh(db_user)
        jwt = JwtUtil.generate_access_token( data={"username": db_user.username} )
        db_user.jwt = jwt
        return db_user
    
    @staticmethod
    def login(db: Session, user: UserLogin):
        user_saved = UserDataSource.get_user_by_username( db=db, username=user.username )
        if user_saved is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales no válidas - username')
        
        if not hash_utils.verify_password( password=user.password, hashed_password=user_saved.password ):
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales no válidas - Password' )
        
        jwt = JwtUtil.generate_access_token( data={ "username": user_saved.username } )
        user_saved.jwt = jwt
        return user_saved
        
        

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(UserModel).filter(UserModel.username == username).first()






