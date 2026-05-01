import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Habits

with st.form("run_form"):
    name = st.text_input("Name")
    done = st.checkbox("Done")
    date = st.date_input("Date")
    submitted = st.form_submit_button("Save")
    if submitted:
        db = SessionLocal()
        new_habits = Habits(
            name=name,
            done=done,
            date=date
        )
        db.add(new_habits)
        db.commit()
        db.close()
        st.success("Saved Habit!")

db = SessionLocal()
habits = db.query(Habits).all()
db.close()
import pandas as pd

df = pd.DataFrame([{
    "name": h.name,
    "done": h.done,
    "date": h.date
} for h in habits])
df = df.sort_values("date")
df = df.sort_values("date", ascending=False)
for date, group in df.groupby("date"):
    st.subheader(str(date))
    st.dataframe(group)
