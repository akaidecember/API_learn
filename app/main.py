from fastapi import FastAPI
from . import models
from .database import engine
from .schemas import *
from .routers import post, users, authenticate

# Creating the tables in the database according to the models specified in models.py
# If the table doesn't exist, it will be created in the postgres DB
models.Base.metadata.create_all(bind=engine)

# Initializing the FastAPI app
app = FastAPI()

# Including the routers in the FastAPI app (users and posts)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(authenticate.router)

# API route for the home page 
@app.get("/")
def read_root():
    return "welcome to the home page"
