from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
# import psycopg2 as db
# from psycopg2.extras import RealDictCursor
# import time
from apps.db import engine, get_db
from sqlalchemy.orm import Session
from apps import models, schemas, utils

#ORM's (object relational mappers) 
#like sqlalchemy still need a driver

#creates the tables in the database based on the models 
#defined in models.py, only creates if they dont already exist
models.Base.metadata.create_all(bind = engine) 


app = FastAPI()

# A query object is a lazy blueprint — no SQL is sent yet, and you can chain filters or run DB-side ops like .update()/.delete() directly, then commit().
# Calling .first() or .all() executes the SQL and loads the result into Python, where you can modify it and persist changes with db.commit().

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump()) #unpacks dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate, id: int, db: Session = Depends(get_db)):
    postquery = db.query(models.Post).filter(models.Post.id == id)
    post = postquery.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    postquery.update(updated_post.model_dump(), synchronize_session=False) #type: ignore
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"message": f"post with id {id} deleted successfully"}

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password) 
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with id {id} not found")
    return user
