from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, utils, models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentication"]
)

# API endpoint for user login
@router.post("/login", response_model=schemas.TokenSchema)
def login(user_cred : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # Verify the password
    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}

