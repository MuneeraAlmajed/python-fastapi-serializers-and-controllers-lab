from sqlalchemy import Column, Integer, String
from .base import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)  # Each username must be unique
    email = Column(String, nullable=False, unique=True)  # Each email must be unique
    password = Column(String, nullable=True)
    
    #Method to hash and store the password
    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
    