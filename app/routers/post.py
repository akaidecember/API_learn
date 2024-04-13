from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import PostCreateSchema, ResponsePostSchema

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# API endpoint for getting all posts
@router.get("/", response_model=list[ResponsePostSchema])
def read_posts(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
               limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    
    # print(limit)
    # Since we are using ORM, we can query the database using the ORM model
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()

    return posts


# API endpoint for creating a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePostSchema)
def create_posts(post : PostCreateSchema, db : Session = Depends(get_db), 
                 current_user : int = Depends(oauth2.get_current_user)):

    # Creating a new post object using the ORM model and setting owner of the post to the curr. logged in user
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# API endpoint for getting a single specified post
@router.get("/{post_id}", response_model=ResponsePostSchema)
def get_post(post_id: int, db : Session = Depends(get_db), 
             current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail = f"Post id : {post_id} not found")
    
    return post


# API endpoint for deleting a single specified post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db : Session = Depends(get_db), 
                current_user : int = Depends(oauth2.get_current_user)):
    
    deleted_post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {post_id} not found")
    
    if current_user.id != db.query(models.Post).filter(models.Post.id == post_id).first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "You do not have permission to delete this post")

    deleted_post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# API endpoint for updating a single specified post
@router.put("/{post_id}", response_model=ResponsePostSchema)
def update_post(post_id : int, new_post : PostCreateSchema, db : Session = Depends(get_db), 
                current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    
    if current_user.id != db.query(models.Post).filter(models.Post.id == post_id).first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "You do not have permission to update this post")
    
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()