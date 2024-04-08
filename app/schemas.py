from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateSchema(PostBaseSchema):
    pass

class ResponsePostSchema(PostBaseSchema):
    title: str
    content: str
    published: bool

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class ResponseUserSchema(BaseModel):
    email: EmailStr
    id: int

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    id: Optional[int] = None