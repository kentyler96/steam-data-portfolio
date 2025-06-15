import requests
import pandas as pd
import psycopg2
import json
from airflow.models import Variable
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from helper_func import to_db
    
def fetch_top_100():
    url = "https://steamspy.com/api.php?request=top100in2weeks"
    df = pd.read_json(url)
    df = df.transpose()
    df = df.reset_index().rename(columns={'index': 'appid'})
    to_db(df, 'steamspy_top_100', 'replace')

    return 'done'

def get_app_ids():
    conn = psycopg2.connect(
        database="steam_dbt_db",
        user="steam_dbt_role",
        password="password",
        host="db",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT appid
        FROM steam_dbt_schema.steamspy_top_100;
    """)
    rows = cur.fetchall()
    app_ids = [row[0] for row in rows]
    cur.close()
    conn.close()
    print(app_ids)
    return app_ids

def get_player_counts(ti, **kwargs):
    start_time = datetime.now()
    app_ids = ti.xcom_pull(task_ids='get_app_ids')

    id_and_player_count = []
    for app_id in app_ids:
        req = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}")
        data = req.json()
        player_count = data.get('response', {}).get('player_count')
        id_and_player_count.append((app_id, player_count))

    df = pd.DataFrame(id_and_player_count, columns=['appid', 'player_count'])
    df['timestamp'] = start_time

    to_db(df, 'top_100_player_counts', 'append')
    return "done"

def get_achievement_names(ti, **kwargs):
    app_ids = ti.xcom_pull(task_ids='get_app_ids')
    id_and_json_data = []
    api_key = Variable.get("STEAM_API_KEY", default_var=None)

    if not api_key:
        raise ValueError("STEAM_API_KEY variable is not set in Airflow Variables under Admin > Variables.")
    
    for app_id in app_ids:
        req = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={api_key}&appid={app_id}")
        data = req.json()
        json_data = data.get('game', {}).get('availableGameStats', {}).get('achievements', [])
        id_and_json_data.append((app_id, json_data))

    df = pd.DataFrame(id_and_json_data, columns=['appid', 'json_data'])
    datatype = {'json_data': JSONB}

    to_db(df, 'achievement_details', 'replace', datatype)
    return "done"

def get_achievement_percentages(ti, **kwargs):
    app_ids = ti.xcom_pull(task_ids='get_app_ids')
    start_time = datetime.now()
    id_and_achievement_percent = []
    for app_id in app_ids:
        req = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={app_id}")
        data = req.json()

        achievements = data.get('achievementpercentages', {}).get('achievements', [])        

        for achievement in achievements:
            id_and_achievement_percent.append(
                (
                app_id,
                achievement['name'],
                achievement['percent']
                )
            )
            
    df = pd.DataFrame(id_and_achievement_percent, columns=['appid', 'name', 'achievement_percent'])
    df['timestamp'] = start_time

    to_db(df, 'achievement_percentages', 'append')
    return 'done'