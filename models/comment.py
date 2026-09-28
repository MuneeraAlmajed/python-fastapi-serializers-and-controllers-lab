from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class CommentModel(BaseModel):


    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(String, nullable=False)

    # Tea Associations:
    tea_id = Column(Integer, ForeignKey('teas.id'), nullable=False)
    tea = relationship('TeaModel', back_populates="comments")
    
    # User Association:
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='comments')