from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schema
from .. import utilities
from .. import models

route = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@route.post("/new_user")
def create_new_user(user_data: schema.new_user_credentials, db: Session = Depends(utilities.get_db)):
    """Add the new user to the database"""
    
    check_query = db.query(models.users).filter(models.users.email == user_data.email).first()
    if check_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_data.email} already have an accountin gym...")
    
    hashed_password = utilities.get_hashed_password(user_data.password)  # Fixed typo
    user_dict = user_data.dict()  # Convert to dictionary
    user_dict["password"] = hashed_password  # Update password

    new_user = models.users(**user_dict)  # Pass the updated dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user_dict


@route.post("/login")
def login(user_data: schema.user_login, db: Session = Depends(utilities.get_db)):
    """login and create a JWT tokens"""
    check_user = db.query(models.users).filter(models.users.email == user_data.email).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_data.email} does not have account...")
    if not utilities.verify_user(user_data.password, check_user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Invalid crediantials ...")
        
    jwt_token = utilities.generate_access_token({"user_id": check_user.id})
    return {"token": jwt_token, "username": check_user.name}