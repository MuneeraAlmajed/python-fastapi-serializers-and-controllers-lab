from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.comment import CommentModel
from models.tea import TeaModel
from serializers.comment import CommentSchema, CreateCommentSchema, UpdateCommentSchema
from serializers.user import UserSchema
from dependencies.get_current_user import get_current_user
from typing import List
from database import get_db

# Initialize the router
router = APIRouter()


@router.get("/teas/{tea_id}/comments", response_model=List[CommentSchema])
def get_comments_for_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    return tea.comments


@router.get("/comments/{comment_id}", response_model=CommentSchema)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.post("/comments/{tea_id}", response_model=CommentSchema)
def create_comment(
    tea_id: int,
    comment: CreateCommentSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user)
):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    new_comment = CommentModel(
        **comment.dict(),
        tea_id=tea_id,
        user_id=user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment: UpdateCommentSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user)
):
    db_comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id
    ).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if not db_comment.user_id == user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    comment_data = comment.dict(exclude_unset=True)

    for key, value in comment_data.items():
        setattr(db_comment, key, value)

    db.commit()
    db.refresh(db_comment)

    return db_comment

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int,
                   db: Session = Depends(get_db),
                   user: UserSchema = Depends(get_current_user)):
    comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if not comment.user_id == user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}