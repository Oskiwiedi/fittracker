import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from db.database import SessionLocal
from db.models import Run
from api.strava import get_strava_runs

if not st.session_state.get("authentication_status"):
    st.error("Please login first!")
    st.stop()

if st.button("Import from Strava"):
    db = SessionLocal()
    db.query(Run).delete()
    db.commit()
    runs_data = get_strava_runs()
    for run in runs_data:
        new_run = Run(
            length=run["distance"],
            time=run["time"],
            date=run["date"]
        )
        db.add(new_run)
    db.commit()
    db.close()
    st.success(f"{len(runs_data)} runs imported!")
    st.rerun()

db = SessionLocal()
runs = db.query(Run).all()
db.close()
import pandas as pd

df = pd.DataFrame([{
    "id": r.id,
    "length": r.length,
    "time": r.time,
    "date": r.date.strftime("%d.%m.%Y")
} for r in runs])
if df.empty:
    st.write("Noch keine Runs eingetragen!")
else:
    for date, group in df.groupby("date"):
            st.subheader(str(date))
            header1, header2, header3 = st.columns([2, 2, 1])
            header1.write("**Length**")
            header2.write("**Time**")
            header3.write("**Delete**")
            for index, row in group.iterrows():
                col1, col2, col3,= st.columns([2, 2, 1])
                col1.write(str(round(row['length'], 2)))
                col2.write(str(round(row['time'], 2)))
                if col3.button("❌", key=f"delete_{row['id']}"):
                    db = SessionLocal()
                    db.query(Run).filter(Run.id == row["id"]).delete()
                    db.commit()
                    db.close()
                    st.rerun()