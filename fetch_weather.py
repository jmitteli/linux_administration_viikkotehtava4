#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import tomllib  

from pathlib import Path

# Luetaan sama secrets-tiedosto kuin Streamlit käyttää
BASE_DIR = Path(__file__).resolve().parent.parent   # ~/myapp
with open(BASE_DIR / "myapp" / ".streamlit" / "secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

db_conf = secrets["mysql_weather"]
owm_conf = secrets["openweather"]

API_KEY = owm_conf["api_key"]
CITY = owm_conf.get("city", "Helsinki")

URL = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)

def main():
    # 1) Hae data API:sta
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    temp = float(data["main"]["temp"])
    desc = data["weather"][0]["description"]
    ts = datetime.now()

    # 2) Talleta MySQL:ään
    conn = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"],
    )
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO owm_weather (city, temperature, description, timestamp)
        VALUES (%s, %s, %s, %s)
        """,
        (CITY, temp, desc, ts),
    )
    conn.commit()
    cur.close()
    conn.close()

    print(f"Tallennettu: {CITY} {temp}°C {desc} @ {ts}")

if __name__ == "__main__":
    main()
