from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from helpers import models, schemas, utils, oauth2
from helpers.database import engine, get_db
from typing import Optional, List
router = APIRouter(
    prefix="/login",
    tags = ["Authentication"]
)
#OAuth2PasswordRequestForm returns: username, password
# when we use OAuth2PasswordRequestForm in Postman we have to send post request with form-data instead of JSON body

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
