from sqlalchemy import Column, Integer, String
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config.environment import JWT_SECRET
import jwt
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)  # Each username must be unique
    email = Column(String, nullable=False, unique=True)  # Each email must be unique
    password = Column(String, nullable=True)
    
    teas = relationship('TeaModel', back_populates='user')
    comments = relationship('CommentModel' , back_populates='user')
    
    #Method to hash and store the password
    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
        
    #Method to verify the password 
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
    
    #Method to generate a JWT token
    def generate_token(self):
        # Define the payload
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),  # Expiration time (1 day)
            "iat": datetime.now(timezone.utc),  # Issued at time
            "sub": str(self.id)  # Subject - the user ID
            
        }
        
        #Create the JWT token
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        return token