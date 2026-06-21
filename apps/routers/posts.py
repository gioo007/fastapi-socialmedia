from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..db import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    if current_user is not None:
        print(current_user.id, current_user.first_name)

    new_post = models.Post(**post.model_dump()) #unpacks dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    postquery = db.query(models.Post).filter(models.Post.id == id)
    post = postquery.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    postquery.update(updated_post.model_dump(), synchronize_session=False) #type: ignore
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"message": f"post with id {id} deleted successfully"}

