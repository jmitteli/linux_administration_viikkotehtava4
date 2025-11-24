#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import tomllib
from pathlib import Path


# Luetaan sama secrets-tiedosto kuin Streamlit käyttää
BASE_DIR = Path(__file__).resolve().parent  # /home/ubuntu/myapp
with open(BASE_DIR / "myapp" / ".streamlit" / "secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

# Käytetään sähköhintoja varten määriteltyä blokkia
db_conf = secrets["mysql_electricity"]

# Spot-hinta API -asetukset
REGION = "FI"
RESOLUTION = 15  # priceResolution=15 -> 15 minuutin tarkkuus

URL = (
    "https://api.spot-hinta.fi/JustNow"
    f"?region={REGION}&priceResolution={RESOLUTION}"
)


def main():
    # 1) Hae data API:sta
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Odotetut kentät vastauksessa:
    #  { "Rank": 71,
    #    "DateTime": "2025-11-24T20:15:00+02:00",
    #    "PriceNoTax": 0.13564,
    #    "PriceWithTax": 0.17023 }
    rank_no = int(data["Rank"])
    dt_str = data["DateTime"]
    price_no_tax = float(data["PriceNoTax"])
    price_with_tax = float(data["PriceWithTax"])

    # Muutetaan DateTime Pythonin datetime-olioksi
    dt = datetime.fromisoformat(dt_str)

    # 2) Talleta MySQL:ään (electricity_db.electricity_price)
    conn = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"],
    )
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO electricity_price (dt, rank_no, price_no_tax, price_with_tax)
        VALUES (%s, %s, %s, %s)
        """,
        (dt, rank_no, price_no_tax, price_with_tax),
    )

    conn.commit()
    cur.close()
    conn.close()

    print(
        f"Tallennettu spot-hinta: {dt} "
        f"(rank={rank_no}, price_with_tax={price_with_tax})"
    )


if __name__ == "__main__":
    main()
