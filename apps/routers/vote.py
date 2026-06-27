from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import delete
from sqlalchemy.orm import Session
from .. import schemas, db, models, oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(db.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exits")

    found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    if (vote.direction == 1):    
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} already voted on post with id {vote.post_id}")
       
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"vote added successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exits")

        db.delete(found_vote)
        db.commit()
        return {"message": f"deleted vote  user-{current_user.id} on post-{vote.post_id} successfully"}

