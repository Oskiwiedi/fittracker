import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Run

if not st.session_state.get("authentication_status"):
    st.error("Please login first!")
    st.stop()

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
    "id": r.id,
    "length": r.length,
    "time": r.time,
    "calories": r.calories,
    "date": r.date.strftime("%d.%m.%Y")
} for r in runs])
if df.empty:
    st.write("Noch keine Runs eingetragen!")
else:
    for date, group in df.groupby("date"):
            st.subheader(str(date))
            header1, header2, header3, header4 = st.columns([2, 2, 2, 1])
            header1.write("**Length**")
            header2.write("**Time**")
            header3.write("**Calories**")
            header4.write("**Delete**")
            for index, row in group.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(str(row['length']))
                col2.write(str(row['time']))
                col3.write(str(row['calories']))
                if col4.button("❌", key=f"delete_{row['id']}"):
                    db = SessionLocal()
                    db.query(Run).filter(Run.id == row["id"]).delete()
                    db.commit()
                    db.close()
                    st.rerun()