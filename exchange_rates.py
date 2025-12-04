import pandas as pd
import requests
import json
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Man nimmt die Daten aus der Currences API
urlCurrencies = "https://v6.exchangerate-api.com/v6/ff3618fa3b4dc517a676a20f/latest/EUR"
response = requests.get(urlCurrencies)

print(response)

dataCurrencies = response.json()

print("/////")

print(dataCurrencies)


# Pretty Printing JSON string back
print(json.dumps(dataCurrencies, indent=4, sort_keys=True))

# Richtig: conversion_rates (nicht conversion_rate) und Syntax für DataFrame-Columns beachten
df = pd.DataFrame(dataCurrencies['conversion_rates'].items(), columns=['currency', 'rate'])

# So fügst du Spalten hinzu:
df['base_euro'] = dataCurrencies['base_code']
df['date'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

print(df)

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")


df.to_sql('exchange_rates', con=engine, if_exists='append', index = False)


print("Success! Data was loaded correctly")