import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import calendar
from datetime import datetime
from dotenv import load_dotenv
from db.database import SessionLocal
from db.models import Workout
from db.models import Run
from db.models import Habits
import plotly.express as px
import streamlit_authenticator as stauth

st.set_page_config(layout="wide")

load_dotenv()
password_hash = os.getenv("PASSWORD_HASH")

config = {
    'credentials': {
        'usernames': {
            'oskar': {
                'name': 'Oskar',
                'password': password_hash
            }
        }
    },
    'cookie': {
        'name': 'fittracker_cookie',
        'key': os.getenv("COOKIE_SECRET", "fallback_key"),
        'expiry_days': 30
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    
    db = SessionLocal()
    workouts = db.query(Workout).all()
    runs = db.query(Run).all()
    habits = db.query(Habits).all()
    db.close()

    st.title("FitTracker")

    month = datetime.now().strftime("%B %Y")
    st.subheader(f"Activities in {month}")

    df_workouts = pd.DataFrame([{
        "date": w.date.strftime("%d.%m.%Y"),
        "type": "Workout"
    } for w in workouts])

    df_runs = pd.DataFrame([{
        "date": r.date.strftime("%d.%m.%Y"),
        "type": "Run"
    } for r in runs])

    df_habits = pd.DataFrame([{
        "date": h.date.strftime("%d.%m.%Y"),
        "type": "Habit"
    } for h in habits])

    if df_workouts.empty:
        df_workouts = pd.DataFrame(columns=["date", "type"])
    if df_runs.empty:
        df_runs = pd.DataFrame(columns=["date", "type"])
    if df_habits.empty:
        df_habits = pd.DataFrame(columns=["date", "type"])

    st.subheader(f"Monthly Overview - {month}")

    heute = datetime.now()
    tage = calendar.monthrange(heute.year, heute.month)[1]

    header = "<tr><th>Activity</th>"
    for tag in range(1, tage + 1):
        header += f"<th>{tag:02d}</th>"
    header += "</tr>"

    gym_row = "<tr><td>Gym</td>"
    for tag in range(1, tage + 1):
        datum = f"{tag:02d}.{heute.month:02d}.{heute.year}"
        gym_done = datum in df_workouts["date"].values
        gym_row += "<td>✅</td>" if gym_done else "<td>☐</td>"
    gym_row += "</tr>"

    run_row = "<tr><td>Run</td>"
    for tag in range(1, tage + 1):
        datum = f"{tag:02d}.{heute.month:02d}.{heute.year}"
        run_done = datum in df_runs["date"].values
        run_row += "<td>✅</td>" if run_done else "<td>☐</td>"
    run_row += "</tr>"

    habit_row = "<tr><td>Habits</td>"
    for tag in range(1, tage + 1):
        datum = f"{tag:02d}.{heute.month:02d}.{heute.year}"
        habit_done = datum in df_habits["date"].values
        habit_row += "<td>✅</td>" if habit_done else "<td>☐</td>"
    habit_row += "</tr>"

    table = f"<table>{header}{gym_row}{run_row}{habit_row}</table>"
    st.markdown("""
    <style>
    table { width: 100%; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(table, unsafe_allow_html=True)

    df_all = pd.concat([df_workouts, df_runs, df_habits])

    if df_all.empty:
        st.write("No activities recorded yet!")
    else:
        fig = px.bar(df_all, x="date", color="type", barmode="group")
        st.plotly_chart(fig)

elif authentication_status == False:
    st.error("Username or password incorrect!")
elif authentication_status is None:
    st.warning("Please enter your credentials.")