from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from . import schemas, db, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

SECRET_KEY = "you could basically put any string in here, but they usually use some secure random hexadecimal one"
ALGORITHM = "HS256" #hashing algorithm used for encoding and decoding the jwt token
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #expiration time for the jwt token in minutes (so user is not logged in forever in this case)

oatuh2_scheme = OAuth2PasswordBearer(tokenUrl= '/login')

def create_access_token(data: dict): #data is paylaod
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #add expiration time to the payload

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        #decode verifies the access token (signature == signature)
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id= str(id))
        #token data for now is just the id of the user, could add more info tho

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oatuh2_scheme), db: Session = Depends(db.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers= {"WWW-Authenticate":"Bearer"})
    thisToken = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == thisToken.id).first()

    return user

    #could return user id directly by the below line
    #return verify_access_token(token, credentials_exception)

#anytime you need user ot be logged in to do smth
#you add a dependency to that function of "user_id: int = Depends(oauth2.get_current_user)"
