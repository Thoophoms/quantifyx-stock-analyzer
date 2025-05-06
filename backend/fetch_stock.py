# Todo: Load modules needed to make API calls, access environment variables, and connect to the database
import requests
import os
from dotenv import load_dotenv
from db import get_connection

# Todo: Load Alpha Vantage API key from .env
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


# Function to fetch stock data for stock symbol like AAPL
def fetch_and_store(symbol):
    # URL for getting the daily price from Alpha Vantage
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    # GET request to API and extracts the relevant part of the JSON response
    response = requests.get(url)
    data = response.json().get("Time Series (Daily)", {})


    # connect to PostgreSQL then prepare for a cursor to execute SQL commands
    conn = get_connection()
    cur = conn.cursor()


    try:
        # insert data into stock_prices table
        # Todo: ON CONFLICT DO NOTHING = avoid duplicate entries when fetching the same stock twice
        for date, values in data.items():
            cur.execute("""
                    INSERT INTO stock_prices (symbol, date, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (symbol, date) DO NOTHING;
                """, (
                    symbol,
                    date,
                    float(values["1. open"]),
                    float(values["2. high"]),
                    float(values["3. low"]),
                    float(values["4. close"]),
                    int(values["5. volume"])
            ))

            # Todo: Safely closed the connection and confirm that the data was saved
            conn.commit()
            print(f"Stored data for {symbol}")
    finally:
        cur.close()
        conn.close()