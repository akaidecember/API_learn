from pydantic import BaseModel, EmailStr


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
