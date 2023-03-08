import sys
sys.path.append("..")
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..helpers import models, schemas, utils
from ..helpers.database import engine, get_db
from typing import Optional, List

router = APIRouter(
  prefix = "/users",
  tags = ['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # can set deafult status code return in the decorator
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User id {} already exists".format(user.email))

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    # add new_post to db, then commit the change
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id {} does not exist".format(id))
    return user