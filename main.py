from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from database import create_db_and_tables, get_session
from models import Ride
from utils import calculate_ride_fare

app = FastAPI()


# automatically create the table in the dataset when startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 1. start riding
@app.post("/ride/start")
def start_ride(user_id: str, session: Session = Depends(get_session)):
    # check if the user already has an active ride
    statement = select(Ride).where(Ride.user_id == user_id).where(Ride.is_active == True)
    active_ride = session.exec(statement).first()
    if active_ride:
        raise HTTPException(status_code=400, detail="User already has an active ride")

    new_ride = Ride(user_id=user_id)
    session.add(new_ride)
    session.commit()
    session.refresh(new_ride)
    return new_ride


# 2. end riding
@app.post("/ride/end/{ride_id}")
def end_ride(ride_id: int, session: Session = Depends(get_session)):
    ride = session.get(Ride, ride_id)
    if not ride or not ride.is_active:
        raise HTTPException(status_code=404, detail="Active ride not found")

    ride.end_time = datetime.now()
    ride.total_cost = calculate_ride_fare(ride.start_time, ride.end_time)
    ride.is_active = False

    session.add(ride)
    session.commit()
    session.refresh(ride)
    return ride


# 3. get riding information
@app.get("/ride/{ride_id}")
def get_ride(ride_id: int, session: Session = Depends(get_session)):
    ride = session.get(Ride, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride session not found")
    return ride


# 4. get current/final fees
@app.get("/ride/{ride_id}/cost")
def get_ride_cost(ride_id: int, session: Session = Depends(get_session)):
    ride = session.get(Ride, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride session not found")

    # if the ride has ended, directly return the fee stored in the database
    if not ride.is_active:
        return {"ride_id": ride_id, "cost": ride.total_cost, "status": "completed"}

    # if the ride is still active, dynamically calculate the fee based on "current time"
    current_time = datetime.now()
    estimated_cost = calculate_ride_fare(ride.start_time, current_time)

    return {
        "ride_id": ride_id,
        "current_cost": estimated_cost,
        "status": "ongoing",
        "duration_minutes": round((current_time - ride.start_time).total_seconds() / 60, 2)
    }