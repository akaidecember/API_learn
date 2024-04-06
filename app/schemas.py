 
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateSchema(PostBaseSchema):
    pass

class ResponseSchema(PostBaseSchema):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
