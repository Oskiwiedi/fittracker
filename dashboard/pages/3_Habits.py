import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Habits

if not st.session_state.get("authentication_status"):
    st.error("Please login first!")
    st.stop()

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
    "id": h.id,
    "name": h.name,
    "done": h.done,
    "date": h.date.strftime("%d.%m.%Y")
} for h in habits])
if df.empty:
    st.write("Noch keine Habits eingetragen!")
else:
    for date, group in df.groupby("date"):
            st.subheader(str(date))
            header1, header2, header3= st.columns([2, 2, 1])
            header1.write("**Name**")
            header2.write("**Done**")
            header3.write("**Delete**")
            for index, row in group.iterrows():
                col1, col2, col3 = st.columns([2, 2, 1])
                col1.write(str(row['name']))
                col2.write(str(row['done']))
                if col3.button("❌", key=f"delete_{row['id']}"):
                    db = SessionLocal()
                    db.query(Habits).filter(Habits.id == row["id"]).delete()
                    db.commit()
                    db.close()
                    st.rerun()
