from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm #has the username and password fields for login
from sqlalchemy.orm import Session

from .. import oauth2
from .. import models, schemas, db, utils

router = APIRouter(tags = ["Authentication"]) #tags are used for separation during documentation

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    token = {"access_token": access_token, "token_type": "bearer"}
    return token #returning the access token and the type of token
