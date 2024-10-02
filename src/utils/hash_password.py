
from passlib.context import CryptContext


class HashPassword:

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
