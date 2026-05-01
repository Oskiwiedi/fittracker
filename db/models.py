from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True)
    exercise = Column(String)
    weight = Column(Float)
    reps = Column(Integer)
    date = Column(DateTime)

class Run(Base):
    __tablename__ = "run"
    id = Column(Integer, primary_key=True)
    length = Column(Float)
    time = Column(Float)
    calories = Column (Integer)
    date = Column(DateTime)

class Habits(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    done = Column(Boolean)
    date = Column(DateTime)