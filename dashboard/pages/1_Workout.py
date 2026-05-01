import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Workout

with st.form("workout_form"):
    exersice = st.text_input("Excersice")
    weight = st.number_input("Weight")
    reps = st.number_input("Reps")
    date = st.date_input("Date") 
    submitted = st.form_submit_button("Save")
    if submitted:
        db = SessionLocal()
        new_workout = Workout(
        exercise=exersice,
        weight=weight,
        reps=reps,
        date=date
        )
        db.add(new_workout)
        db.commit()
        db.close()
        st.success("Saved Workout")

db = SessionLocal()
workouts = db.query(Workout).all()
db.close()
import pandas as pd

df = pd.DataFrame([{
    "exercise": w.exercise,
    "weight": w.weight,
    "reps": w.reps,
    "date": w.date
} for w in workouts])
df = df.sort_values("date")
df = df.sort_values("date", ascending=False)
for date, group in df.groupby("date"):
    st.subheader(str(date))
    st.dataframe(group)