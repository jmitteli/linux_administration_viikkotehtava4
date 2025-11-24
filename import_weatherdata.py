import pandas as pd
from sqlalchemy import create_engine

# ---- ASETUKSET: MUOKKAA NÄMÄ ----
DB_USER = "käyttäjäsi"
DB_PASS = "salasanasi"
DB_HOST = "localhost"         # yleensä localhost
DB_NAME = "tietokannan_nimi"
TABLE_NAME = "weatherdata"    # taulun nimi
CSV_PATH = "weatherdata.csv"  # polku csv:hen
# ---------------------------------


def main():
    # Lue csv
    df = pd.read_csv(CSV_PATH)

    # Nimeä sarakkeet tietokantaystävällisiksi
    df = df.rename(columns={
        "Havaintoasema": "station",
        "Vuosi": "year",
        "Kuukausi": "month",
        "Päivä": "day",
        "Aika [Paikallinen aika]": "time_local",
        "Ilman lämpötila [°C]": "temp_c",
    })

    # Luo yhteys MySQL/MariaDB:hen
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )

    # Kirjoita data tauluun (luo taulun automaattisesti, jos sitä ei ole)
    with engine.begin() as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    print("Valmis! CSV on nyt taulussa", TABLE_NAME)


if __name__ == "__main__":
    main()
