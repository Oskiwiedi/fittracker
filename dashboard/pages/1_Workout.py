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
    "id": w.id,
    "exercise": w.exercise,
    "weight": w.weight,
    "reps": w.reps,
    "date": w.date.strftime("%d.%m.%Y")
} for w in workouts])
if df.empty:
    st.write("Noch keine Workout eingetragen!")
else:
    for date, group in df.groupby("date"):
            st.subheader(str(date))
            header1, header2, header3, header4 = st.columns([2, 2, 2, 1])
            header1.write("**Exercise**")
            header2.write("**Weight**")
            header3.write("**Reps**")
            header4.write("**Delete**")
            for index, row in group.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(str(row['exercise']))
                col2.write(str(row['weight']))
                col3.write(str(row['reps']))
                if col4.button("❌", key=f"delete_{row['id']}"):
                    db = SessionLocal()
                    db.query(Workout).filter(Workout.id == row["id"]).delete()
                    db.commit()
                    db.close()
                    st.rerun()