from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, utils
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import ResponseUserSchema, UserCreateSchema

router = APIRouter(
    prefix="/users"
)

# API endpoint for creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema)
def create_user(user : UserCreateSchema, db : Session = Depends(get_db)):

    # Hashing the password before storing it in the DB
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# API endpoint for getting specified user
@router.get("/{user_id}", response_model=ResponseUserSchema)
def get_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return user