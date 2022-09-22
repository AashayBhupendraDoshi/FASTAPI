from logging import raiseExceptions
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(vote: schemas.Vote, db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user)):

    buff = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not buff:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Post does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_data.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT,
                            detail="Already Voted")
        new_vote = models.Vote(post_id = vote.post_id, user_id = user_data.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Vote Does Not Exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'successfully deleted vote'}
