from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .schemas import *
from .routers import post, users, authenticate, vote

# Creating the tables in the database according to the models specified in models.py
# If the table doesn't exist, it will be created in the postgres DB
# Commented because using alembic for migrations
# models.Base.metadata.create_all(bind=engine)

# Initializing the FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including the routers in the FastAPI app (users and posts)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(authenticate.router)
app.include_router(vote.router)

# API route for the home page 
@app.get("/")
def read_root():
    return "welcome to the home page"
