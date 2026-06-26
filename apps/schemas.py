from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel): #extends BaseModel from pydantic
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    date: datetime
    owner_id: int
    class Config:
        from_attributes = True #new way for orm_mode = true
        #tells pydantic to read data from the our ORM (sqlalchemy) models and not just dicts, allows us to return sqlalchemy models directly and pydantic will know how to read them and convert them to the response model

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
