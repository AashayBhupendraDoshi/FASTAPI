from ast import Try
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

# OAuth2PasswordBearer e3ssentially tells Oauth2 where to fetch the token from
# tokenURI is the uri where the token will be sent in th header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET KEY
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
# HASHING ALGORITHM
ALGORITHM = settings.ALGORITHM
# EXPIRATION TIME
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    # This function created a jwt access token for the user
    to_encode = data.copy() 

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    # This function decodes and verifies the acess token sent by the user
    # using the token itself, the algorithm and the secred key.
    try:
        payload = jwt.decode(token=token, key = SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> schemas.UserOut:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=
    "Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    buff = db.query(models.User).filter(models.User.id == token.id).first()
    if buff is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    
    return buff
