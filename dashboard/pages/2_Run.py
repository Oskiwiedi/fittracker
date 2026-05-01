import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Run

with st.form("run_form"):
    length = st.number_input("Length (km)")
    time = st.number_input("Time (min)")
    calories = st.number_input("Calories")
    date = st.date_input("Date")
    submitted = st.form_submit_button("Save")
    if submitted:
        db = SessionLocal()
        new_run = Run(
            length=length,
            time=time,
            calories=calories,
            date=date
        )
        db.add(new_run)
        db.commit()
        db.close()
        st.success("Saved Run!")

db = SessionLocal()
runs = db.query(Run).all()
db.close()
import pandas as pd

df = pd.DataFrame([{
    "length": r.length,
    "time": r.time,
    "calories": r.calories,
    "date": r.date
} for r in runs])
df = df.sort_values("date")
df = df.sort_values("date", ascending=False)
for date, group in df.groupby("date"):
    st.subheader(str(date))
    st.dataframe(group)