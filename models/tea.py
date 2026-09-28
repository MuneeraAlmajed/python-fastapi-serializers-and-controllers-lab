from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Associations
from .comment import CommentModel
from .base import BaseModel
from .user import UserModel


class TeaModel(BaseModel):

    def __str__(self):
        return f"{self.id}: {self.name}"

    __tablename__ = "teas"

    id = Column(Integer, primary_key=True, index=True)


    name = Column(String, unique=True)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('UserModel', back_populates='teas')
    comments = relationship('CommentModel', back_populates="tea")