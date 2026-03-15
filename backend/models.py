from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserIn(BaseModel):
    name : str
    email :EmailStr
    username : str
    password:str

class UserOut(BaseModel):
    user_id: Optional[int] = None
    name:str
    username:str
    email:EmailStr

class LoginReq(BaseModel):
    username : str
    password : str

class PostCreate(BaseModel):
    username : Optional[str] = None
    post_id : Optional[int] = None
    content_type : str
    title : str
    post : str

class PostShow(BaseModel):
    post_id : Optional[int] = None
    username : str
    content_type: str
    title: str
    post: str
    created_at: datetime = Field(default_factory=datetime.now)


