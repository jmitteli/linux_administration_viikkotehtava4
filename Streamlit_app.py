import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


@st.cache_data(ttl=60)
def load_owm_data():
    """Lataa OpenWeather-datan owm_weather-taulusta."""
    db_conf = st.secrets["mysql"]

    conn = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"],
    )

    query = """
        SELECT city, temperature, description, timestamp
        FROM owm_weather
        ORDER BY timestamp
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # Muutetaan aikaleimat oikeaksi datetime-tyypiksi ja järjestetään
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    return df


def main():
    st.title("Helsinki – lämpötilan kehitys")

    owm_df = load_owm_data()

    if owm_df.empty:
        st.warning("Tietokannassa ei ole vielä OpenWeather-dataa.")
        return

    # 1) Lämpötila käyränä
    fig = px.line(
        owm_df,
        x="timestamp",
        y="temperature",
        labels={"timestamp": "Aika", "temperature": "Lämpötila (°C)"},
        title="Lämpötilan kehitys Helsingissä (OpenWeather)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2) Taulukko: 100 uusinta päivitystä
    st.subheader("Viimeisimmät 100 päivitystä")

    last100 = (
        owm_df.sort_values("timestamp", ascending=False)
              .head(100)
              .reset_index(drop=True)
    )
    last100 = last100[["timestamp", "city", "temperature", "description"]]

    st.dataframe(last100)


if __name__ == "__main__":
    main()
