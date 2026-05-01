import os
from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

client = Client()
client.access_token = os.getenv("STRAVA_ACCESS_TOKEN")
client.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
client.token_expires_at = None

def get_strava_runs():
    activities = client.get_activities()
    runs = []
    for activity in activities:
        if activity.type == "Run":
            print(activity.kilojoules)
            runs.append({
                "name": activity.name,
                "distance": round(float(activity.distance) / 1000, 2),
                "time": round(int(activity.moving_time) / 60, 2),
                "date": activity.start_date_local.strftime("%Y-%m-%d")
            })
    return runs