from passlib.context import CryptContext

# Default hashing algo. to be used is bcrypt. This is used to hash the password in the DB for security.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password : str):
    return password_context.hash(password)
