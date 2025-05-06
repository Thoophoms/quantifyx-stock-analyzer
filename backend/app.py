from os import close

from flask import Flask, jsonify, request
# fetch stock data from Alpha Vantage
from fetch_stock import fetch_and_store
# database connection function
from db import get_connection
# import CORS to allow frontend to access Flask API
from flask_cors import CORS

# initialize flask application
app = Flask(__name__)
CORS(app)


# Todo 1: Calls fetch_and_store() to get data from Alpha Vantage and insert into the database
@app.route("/api/fetch/<symbol>", methods=["GET"])
def fetch(symbol):
    try:
        fetch_and_store(symbol) # fetch and save into DB
        return jsonify({"message": f"✅ Data for {symbol} fetched and stored."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Todo 2: Return price history for a symbol from DB
@app.route("/api/price-history/<symbol>", methods=["GET"])
def price_history(symbol):
    try:
        # connect database
        conn = get_connection()
        cur = conn.cursor()

        # Todo: Queries the database for the symbol's price history and return it as JSON
        cur.execute("""
        SELECT date, open, high, low, close, volume
        FROM stock_prices
        WHERE symbol = %s
        ORDER by date ASC
        """, (symbol.upper(),)) # tuple with tailing comma

        # fetch all rows returned by the query
        rows = cur.fetchall()

        # Todo 3: Convert rows to list of dictionaries
        data = [
            {
                "date": date.isoformat(), # to string
                "open": float(open_),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": int(volume)
            }
            for (date, open_, high, low, close, volume) in rows
        ]

        # close DB connection
        cur.close()
        conn.close()


        # Todo 4: Return result in JSON format
        return jsonify({
            "symbol": symbol.upper(),
            "data": data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Only run the server if the script os executed directly
if __name__ == "__main__":
    app.run(debug=True) # dedug = True -- to show error message