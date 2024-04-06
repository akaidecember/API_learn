from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import PostCreateSchema, ResponsePostSchema

router = APIRouter(
    prefix="/posts"
)

# API endpoint for getting all posts
@router.get("/", response_model=list[ResponsePostSchema])
def read_posts(db : Session = Depends(get_db)):

    # Since we are using ORM, we can query the database using the ORM model
    posts = db.query(models.Post).all()

    return posts


# API endpoint for creating a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePostSchema)
def create_posts(post : PostCreateSchema, db : Session = Depends(get_db)):

    # Creating a new post object using the ORM model
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# API endpoint for getting a single specified post
@router.get("/{post_id}", response_model=ResponsePostSchema)
def get_post(post_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post id : {post_id} not found")
    return post


# API endpoint for deleting a single specified post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db : Session = Depends(get_db)):
    deleted_post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {post_id} not found")
    deleted_post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# API endpoint for updating a single specified post
@router.put("/{post_id}", response_model=ResponsePostSchema)
def update_post(post_id : int, new_post : PostCreateSchema, db : Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()