from fastapi import APIRouter, Depends, HTTPException

# Models
from models.tea import TeaModel

# Serializers & Validations
from serializers.tea import TeaSchema, CreateTeaSchema, UpdateTeaSchema
from serializers.user import UserSchema
from typing import List

# DB
from sqlalchemy.orm import Session
from database import get_db

from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get('/teas', response_model=List[TeaSchema])
def get_teas(db: Session = Depends(get_db)):
  teas = db.query(TeaModel).all()

  return teas

@router.get("/teas/{tea_id}", response_model=TeaSchema)
def get_single_tea(tea_id: int, db: Session = Depends(get_db)):
  tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

  if not tea:
    raise HTTPException(status_code=404, detail="Cannot find Tea")

  return tea


@router.post("/teas", response_model=TeaSchema, status_code=201)
def create_tea(tea: CreateTeaSchema, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):
    try:
      new_tea = TeaModel(**tea.dict(), user_id = user.id)# Convert Pydantic model to SQLAlchemy model
      db.add(new_tea)
      db.commit() # basicallt model.save()
      db.refresh(new_tea)
    except:
      raise HTTPException(status_code=422, detail='Unprocessable Entity')

    return new_tea



@router.put("/teas/{tea_id}", response_model=TeaSchema)
def update_tea(tea_id: int, 
               tea: UpdateTeaSchema, 
               db: Session = Depends(get_db), 
               user: UserSchema = Depends(get_current_user)):

    # Find the tea to update
    db_tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    # If tea was not found, raise an error
    if not db_tea:
      raise HTTPException(status_code=404, detail="Tea not found")
    
    if not db_tea.user_id == user.id:
      raise HTTPException(status_code=403, detail="Forbidden")


    tea_data = tea.dict(exclude_unset=True)

    # loop thru the dict and replace the value for the key
    for key, value in tea_data.items():
       setattr(db_tea, key, value)

    db.commit()
    db.refresh(db_tea)

    return db_tea

@router.delete("/teas/{tea_id}", status_code=204)
def delete_tea(tea_id: int, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):

    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    
    if not tea:
      raise HTTPException(status_code=404, detail="Tea not found")
    
    if not tea.user_id == user.id:
          raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(tea)
    db.commit()

    return None
    # return {"message": f"Tea with ID {tea_id} has been deleted"}