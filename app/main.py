from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine
from . import models
from .utilities import get_db, get_current_user
from .routes import auth, gym

# handle the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.route)
app.include_router(gym.route)

@app.get("/")
def root():
    return {"message": "gym app is working"}

@app.get("/users")
def users(db:Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    res = db.query(models.users).filter(models.users.role == "trainer").all()
    print(user_id)
    return res