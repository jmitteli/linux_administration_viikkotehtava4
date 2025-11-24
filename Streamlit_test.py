# Streamlit_test.py
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    # sama hakemisto kuin tämä .py-tiedosto
    df = pd.read_csv("weatherdata.csv")

    # Tee yhdestä sarakkeesta aikaleima
    df["datetime"] = pd.to_datetime(
        df["Vuosi"].astype(str)
        + "-"
        + df["Kuukausi"].astype(str)
        + "-"
        + df["Päivä"].astype(str)
        + " "
        + df["Aika [Paikallinen aika]"]
    )

    # Järjestetään ajan mukaan varmuuden vuoksi
    df = df.sort_values("datetime")
    return df


def main():
    st.title("Lämpötilan kehitys")

    df = load_data()

    fig = px.line(
        df,
        x="datetime",
        y="Ilman lämpötila [°C]",
        labels={
            "datetime": "Aika",
            "Ilman lämpötila [°C]": "Lämpötila (°C)",
        },
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()