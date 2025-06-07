from .database import SessionLocal
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    """Hash the password and return the hashed value"""
    return password_context.encrypt(password)

def verify_user(check_password, hashed_password):
    """Verify the  password"""
    return password_context.verify(check_password, hashed_password)


##########################################################################
# JWT
##########################################################################


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "23rtfdsw3refdsw345tgf"  # Store securely
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 60 minutes


def generate_access_token(claims: str):
    """generate the valid jwt token"""
    payload = claims.copy()
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token, error):
    """verify the token and then return the user id"""
    
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = encoded_jwt.get("user_id")
        
        if not user_id:
            raise error
    except JWTError:
        raise error
    
    return user_id

def get_current_user(token: str = Depends(oauth2_schema)):
    
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access...")
    
    return verify_access_token(token, error)