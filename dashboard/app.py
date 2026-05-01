import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from datetime import datetime
from db.database import SessionLocal
from db.models import Workout
from db.models import Run
from db.models import Habits
import plotly.express as px

db = SessionLocal()
workouts = db.query(Workout).all()
runs = db.query(Run).all()
habits = db.query(Habits).all()
db.close()

st.title("FitTracker")
st.write("More detailed information will be provided here later")

monat = datetime.now().strftime("%B %Y")
st.subheader(f"Aktivitäten im {monat}")

df_workouts = pd.DataFrame([{
    "date": w.date,
    "type": "Workout"
} for w in workouts])

df_runs = pd.DataFrame([{
    "date": r.date,
    "type": "Run"
} for r in runs])

df_habits = pd.DataFrame([{
    "date": h.date,
    "type": "Habit"
} for h in habits])

df_all = pd.concat([df_workouts, df_runs, df_habits])

fig = px.bar(df_all, x="date", color="type", barmode="group")
st.plotly_chart(fig)