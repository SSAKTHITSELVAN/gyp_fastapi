from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schema
from .. import utilities
from .. import models
from sqlalchemy import desc

route = APIRouter(
    prefix="/gym",
    tags=["Authentication"]
)


@route.get("/status")
def check_gym_status(db: Session = Depends(utilities.get_db), user_id: int = Depends(utilities.get_current_user)):
    """Verify the gym status(open or close) only for --Students"""
    
    user_role_check = db.query(models.users).filter(models.users.id == user_id).first()
    if user_role_check.role != 'Student':
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="your on the bad track")
    
    # Query the most recent gym status entry
    latest_status = db.query(models.Gym_status).order_by(
        desc(models.Gym_status.updated_at)
    ).first()
    
    gym_master = db.query(models.users).filter(models.users.id == latest_status.updated_by).first()
    
    if not latest_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No gym status available(be student to see)")
    
    return {"status": latest_status.status, "updated_by": gym_master.name ,"updated_at": latest_status.updated_at}


@route.post("/updates")
def gym_updates_by_master(current_status: schema.gym_status_update, db: Session = Depends(utilities.get_db), user_id: int = Depends(utilities.get_current_user)):
    """Master update the status of the gym daily(morning and evening)"""
    user_role_check = db.query(models.users).filter(models.users.id == user_id).first()
    if user_role_check.role != 'trainer':
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="your on the bad track(be trainer to update)")
    
    new_update = models.Gym_status(status=current_status.status, updated_by=user_id)
    db.add(new_update)
    db.commit()
    db.refresh(new_update)
    return new_update
