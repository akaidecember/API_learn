from http.client import HTTPException
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title1", "content": "content1", "published": True, "id": 1},
            {"title": "title2", "content": "random", "published": False, "id": 2},]
 

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def read_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : PostSchema):
    post_dict = post.dict()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"new_post": post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):  
    for post in my_posts:
        if post['id'] == post_id:
            return {"data" : post}
    raise HTTPException(status_code=404, detail = f"Post id : {post_id} not found")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int):
    for post in my_posts:
        if post['id'] == post_id:
            my_posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail = f"Post {post_id} not found")


@app.put("/posts/{post_id}")
def update_post(post_id : int, new_post : PostSchema):
    for index, post in enumerate(my_posts):
        if post['id'] == post_id:
            my_posts[index] = new_post.dict()
            my_posts[index]['id'] = post_id  
            return {"data": my_posts[index]}
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")