from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

# Define Data object (like java object) using pydantic BaseModel
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class PostBase(BaseModel):
    title: str
    content: str
    # Adding Default Value to the Field
    published: bool = True
    # Adding Optional Field with default value None
    # rating: Optional[int] = None 

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    # orm_mode = True, sets pydantic to go through sqalchemy orm models as well
    # rather than purely dictionaries
    # so it checks object.key along with object["key"] 
    class Config:
        orm_mode = True

class PostComplete(BaseModel):
    Post: PostResponse
    Votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1,)


