from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class ResponseUserSchema(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateSchema(PostBaseSchema):
    pass

class ResponsePostSchema(PostBaseSchema):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUserSchema

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    id: Optional[int] = None

class VoteSchema(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOutSchema(BaseModel):
    Post: ResponsePostSchema
    votes: int
