from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #use bcrypt for hashing algorithm

def hash_password(password: str):
    return pwd_context.hash(password)
    #hash password using password context

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    #built in method to verify passwords from passlib