from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import *

# Creating the tables in the database according to the models specified in models.py
# If the table doesn't exist, it will be created in the postgres DB
models.Base.metadata.create_all(bind=engine)

# Initializing the FastAPI app
app = FastAPI()

# API route for the home page 
@app.get("/")
def read_root():
    return "welcome to the home page"


# API endpoint for getting all posts
@app.get("/posts", response_model=list[ResponsePostSchema])
def read_posts(db : Session = Depends(get_db)):

    # Since we are using ORM, we can query the database using the ORM model
    posts = db.query(models.Post).all()

    return posts


# API endpoint for creating a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=ResponsePostSchema)
def create_posts(post : PostCreateSchema, db : Session = Depends(get_db)):

    # Creating a new post object using the ORM model
    # **post.dict() will unpack the post object into a dictionary
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# API endpoint for getting a single specified post
@app.get("/posts/{post_id}", response_model=ResponsePostSchema)
def get_post(post_id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post id : {post_id} not found")
    return post


# API endpoint for deleting a single specified post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db : Session = Depends(get_db)):
    deleted_post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {post_id} not found")
    deleted_post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# API endpoint for updating a single specified post
@app.put("/posts/{post_id}", response_model=ResponsePostSchema)
def update_post(post_id : int, new_post : PostCreateSchema, db : Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


# API endpoint for creating a new user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema)
def create_user(user : UserCreateSchema, db : Session = Depends(get_db)):

    # Hashing the password before storing it in the DB
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# API endpoint for getting specified user
@app.get("/users/{user_id}", response_model=ResponseUserSchema)
def get_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return user

