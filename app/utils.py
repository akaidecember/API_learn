from passlib.context import CryptContext

# Default hashing algo. to be used is bcrypt. This is used to hash the password in the DB for security.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash the password
def hash(password : str):
    return password_context.hash(password)


# Function to verify the password
def verify_password(plain_password : str, hashed_password : str):
    return password_context.verify(plain_password, hashed_password)