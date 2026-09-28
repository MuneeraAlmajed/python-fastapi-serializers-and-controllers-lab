from pydantic import BaseModel

class UserRegistrationSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)

# Schema for returning user data (without exposing the password)
class UserSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True