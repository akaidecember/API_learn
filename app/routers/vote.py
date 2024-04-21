from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, oauth2, schemas, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.VoteSchema, db : Session = Depends(database.get_db), 
         current_user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id: {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    new_vote = vote_query.first()
    if vote.dir == 1:
        if new_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has already voted on post: {vote.post_id}")
        db.add(models.Vote(user_id = current_user.id, post_id = vote.post_id))
        db.commit()
        return {"message" : "Vote registered"}
    else:
        if not new_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user: {current_user.id} has not voted on post: {vote.post_id}")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message" : "Vote removed"}