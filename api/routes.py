from fastapi import APIRouter
from db.database import SessionLocal
from db.models import Workout
from db.models import Run
from db.models import Habits
from pydantic import BaseModel
from datetime import date
from api.strava import get_strava_runs
from api.strava import get_strava_runs

class WorkoutCreate(BaseModel):
    exercise: str
    weight: float
    reps: int
    date: date

class RunCreate(BaseModel):
    length: float
    time: float
    calories: int
    date: date

class HabitsCreate(BaseModel):
    name: str
    done: bool
    date: date

router = APIRouter()

@router.get("/workouts")
def get_workouts():
    db = SessionLocal()
    workouts = db.query(Workout).all()
    db.close()
    return workouts

@router.get("/runs")
def get_runs():
    db = SessionLocal()
    runs = db.query(Run).all()
    db.close()
    return runs

@router.get("/habits")
def get_habits():
    db = SessionLocal()
    habits = db.query(Habits).all()
    db.close()
    return habits   

@router.post("/workouts")
def create_workout(workout: WorkoutCreate):
    db = SessionLocal()
    new_workout = Workout(
        exercise=workout.exercise,
        weight=workout.weight,
        reps=workout.reps,
        date=workout.date
    )
    db.add(new_workout)
    db.commit()
    db.close()
    return {"message": "Workout created!"}

@router.post("/runs")
def create_run(run: RunCreate):
    db = SessionLocal()
    new_run = Run(
        length=run["distance"],
        time=run["time"],
        calories=0,
        date=run["date"]
    )
    db.add(new_run)
    db.commit()
    db.close()
    return {"message": "Run created!"}

@router.post("/habits")
def create_habit(habit: HabitsCreate):
    db = SessionLocal()
    new_habit = Habits(
        name=habit.name,
        done=habit.done,
        date=habit.date
    )
    db.add(new_habit)
    db.commit()
    db.close()
    return {"message": "Habit created!"}

@router.get("/strava/runs")
def strava_runs():
    return get_strava_runs()

@router.post("/strava/import")
def import_strava_runs():
    runs = get_strava_runs()
    db = SessionLocal()
    for run in runs:
        new_run = Run(
            length=run["distance"],
            time=run["time"],
            calories=0,
            date=run["date"]
        )
        db.add(new_run)
    db.commit()
    db.close()
    return {"message": f"{len(runs)} runs imported!"}