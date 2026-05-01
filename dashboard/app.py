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