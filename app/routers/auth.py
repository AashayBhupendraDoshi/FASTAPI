from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    # prefix="/users",
    tags=["authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm is a form to directly take in login credentials from the user
    # OAuth2PasswordRequestForm returns a dict with two fields:
    # username (str) and password (str)
    buff = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if buff is None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, buff.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    # Data sent to create can be anything.
    # Note that jwt tokens are not encrypted and hance anyone will be able to read
    # Contents of the jwt data payload
    access_token = oauth2.create_access_token(data = {"user_id": buff.id})
    return {"access_token": access_token, "token_type": "bearer"}