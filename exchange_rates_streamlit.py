import pandas as pd 
import streamlit as st
from sqlalchemy import create_engine, text # create_engine fehlte
from dotenv import load_dotenv
import os
import plotly.express as px # Für die Visualisierung

# 1. Dotenv initialisieren (Klammern wichtig!)
load_dotenv() 

# Variablen laden
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# 2. Connection String (Beachte: Dein Code nutzt PostgreSQL Syntax, oben sprachen wir über SQL Server)
# Falls du SQL Server nutzt, ändere "postgresql+psycopg2" zu "mssql+pyodbc"
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

st.title("💹 Wechselkurs Monitor")


auswahl = pd.read_sql("""
                      
                      SELECT DISTINCT currency
                        FROM exchange_rates
                      
                      """, 
                         engine)['currency'].tolist()

#Möchte nach einer Bestimmten Währug filtern
selected_currency = st.selectbox("Choose one currency", 
                                 options=auswahl, 
                                 index=auswahl.index("USD")
             )

# 3. SQL Query (Flexibler gestaltet, um einen Verlauf zu zeigen)
# Wir holen die letzten 30 Tage statt nur heute, um ein Diagramm zu zeichnen
query = f"""
SELECT date, base_euro, rate, currency 
FROM exchange_rates 
WHERE currency = '{selected_currency}'
ORDER BY date ASC
"""


try:
    # Daten laden
    df = pd.read_sql(query, engine)

    # --- Anzeige Metrik ---
    latest_rate = df.iloc[-1]['rate']
    st.metric(label=f"Aktueller {selected_currency} Kurs", value=f"{latest_rate}")

    euros_value = st.number_input("Enter VALUE in EUROS:")
    # Calculating value from Euros in the other currency
    total_currency = latest_rate * euros_value
    st.metric(label=f"Umberechnung {euros_value} Euros in {selected_currency}", value=f"{total_currency}")


    # 4. Plotly Diagramm (Nachbau vom Screenshots)
    fig = px.line(df, x='date', y='rate', title='Trend: Summe von rate nach date', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 5. Tabelle anzeigen
    st.subheader("Rohdaten aus der Datenbank")
    st.write(df)

except Exception as e:
    st.error(f"Verbindungsfehler: {e}")

    