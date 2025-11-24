import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


@st.cache_data(ttl=60)
def load_owm_data():
    """Lataa OpenWeather-datan owm_weather-taulusta."""
    db_conf = st.secrets["mysql_weather"]

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

@st.cache_data(ttl=60)
def load_price_data():
    """Lataa sähkön spot-hinnan electricity_price-taulusta."""
    db_conf = st.secrets["mysql_electricity"]

    conn = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"],
    )

    query = """
        SELECT dt, rank_no, price_no_tax, price_with_tax
        FROM electricity_price
        ORDER BY dt
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df["dt"] = pd.to_datetime(df["dt"])
    df = df.sort_values("dt")

    return df


def main():

    # Päivitä sivu 5 minuutin välein (300 sekuntia)
    st.markdown(
        """
        <meta http-equiv="refresh" content="300">
        """,
        unsafe_allow_html=True,
    )

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

    # --- SÄHKÖHINTA ---
    st.header("Sähkön spot-hinta (FI)")

    price_df = load_price_data()

    if price_df.empty:
        st.warning("Tietokannassa ei ole vielä sähkön hintadataa.")
        return

    # Käyrä hinnasta (sis. verot)
    fig_price = px.line(
        price_df,
        x="dt",
        y="price_with_tax",
        labels={"dt": "Aika", "price_with_tax": "Hinta (€/kWh)"},
        title="Sähkön spot-hinta (sis. verot)",
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # Taulukko: 20 viimeisintä hintaa
    st.subheader("Viimeisimmät 20 hintaa")

    last20 = (
        price_df.sort_values("dt", ascending=False)
                .head(20)
                .reset_index(drop=True)
    )
    last20 = last20[["dt", "rank_no", "price_no_tax", "price_with_tax"]]

    st.dataframe(last20)

if __name__ == "__main__":
    main()
