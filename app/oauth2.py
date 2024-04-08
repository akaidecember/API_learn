import json
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

conf_filepath = 'config/secret.json'

def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = read_config(conf_filepath)

SECRET_KEY = config['secret']['key']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data : dict):

    # Create a copy of the data to encode, don't want to manipulate og copy
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Update teh dict expire field
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Verify the token
def verify_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenDataSchema(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    # Create a credentials exception
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
