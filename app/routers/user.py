from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user.password = utils.hash(new_user.password)
    buff = models.User(**new_user.dict())
    db.add(buff)
    db.commit()
    db.refresh(buff)
    return buff


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def create_user(id: int, db: Session = Depends(get_db)):

    buff = db.query(models.User).filter(models.User.id == id).first()

    if buff is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    
    return buff