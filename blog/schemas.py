from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config:
        from_attributes = True


class Blog(BaseModel):
    title: str  
    body: str
    published: Optional[bool]
    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    # if you want to get all columns except id just live the first part empty
    title: str  
    body: str
    creator: ShowUser
    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
 
class TokenData(BaseModel):
    email: str = None