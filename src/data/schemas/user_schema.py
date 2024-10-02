from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    
class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    name: str
    password: str
    
    
class UserResponse(UserBase):
    id: int
    name: str
    jwt: str
    
class UserSchema(UserCreate):
    id: int
    class Config:
        orm_mode = True

