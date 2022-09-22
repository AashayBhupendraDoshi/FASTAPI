from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/", response_model=List[schemas.PostComplete])
# Always import get_db function for interact with DB
# get_db creates a session to query the db
# Depends() makes get_db a dependency
async def get_posts(db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user),
                    # Adding path parameters
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # .all() is analogus to fetchall() in psycopg
    # print(user_data)
    # buff = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # .label labels the query with the input name
    # In sequel alchemy this by default is a left inner join
    # Set isouter=True for outer join
    buff = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')
                    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                    ).group_by(models.Post.id
                    ).filter(models.Post.title.contains(search)
                    ).limit(limit).offset(skip
                    ).all()
    print(buff)
    return buff


@router.get("/{id}", response_model=schemas.PostComplete)
async def get_post_by_id(id: int, db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user)):
    # .first() is analogus to fetchone() in psycopg2
    # buff = db.query(models.Post).filter(models.Post.id == id).first()
    buff = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')
                    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                    ).group_by(models.Post.id
                    ).filter(models.Post.id == id).first()
    # If post does not exist raise exception
    if buff is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    return buff
    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# user_id: int = Depends(oauth2.get_current_user) is an extra dependency that required the user to have passed a valid bearer jwt token
# in order to use the function
async def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user)):
    # buff = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)
    # ** converts the dict into keyword arguments to function call (**kwargs)
    # print(user_data.id)
    buff = models.Post(user_id=user_data.id, **new_post.dict())
    # Commit the changes to the DB
    db.add(buff)
    db.commit()
    db.refresh(buff)
    return buff


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int, db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user)):
    buff = db.query(models.Post).filter(models.Post.id == id)
    # If post does not exist raise exception
    if buff.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    
    if buff.first().user_id != user_data.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="User Not authorised for this action")
    buff.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def update_post_by_id(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_data: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    buff = db.query(models.Post).filter(models.Post.id == id)
    
    if buff.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")

    if buff.first().user_id != user_data.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="User Not authorised for this action")

    buff.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return buff.first()