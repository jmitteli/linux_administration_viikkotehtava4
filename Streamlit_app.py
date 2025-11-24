import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px


@st.cache_data
def load_data():
    # luetaan tiedot secretsistä
    db_conf = st.secrets["mysql"]
    user = db_conf["user"]
    password = db_conf["password"]
    host = db_conf["host"]
    database = db_conf["database"]

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
    )

    query = """
        SELECT station, year, month, day, time_local, temp_c
        FROM weatherdata
    """
    df = pd.read_sql(query, engine)

    df["datetime"] = pd.to_datetime(
        df["year"].astype(str)
        + "-"
        + df["month"].astype(str)
        + "-"
        + df["day"].astype(str)
        + " "
        + df["time_local"] + ":00"
    )
    df = df.sort_values("datetime")
    return df


def main():
    st.title("Lämpötilan kehitys – Oulu Vihreäsaari satama")
    df = load_data()

    fig = px.line(
        df,
        x="datetime",
        y="temp_c",
        labels={"datetime": "Aika", "temp_c": "Lämpötila (°C)"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[["datetime", "temp_c"]])


if __name__ == "__main__":
    main()
