from flask import Flask, jsonify
import random
from datetime import datetime

# Initialize the Flask application
# This creates a simple web server.
app = Flask(__name__)

# --- 1. Mock Database for Financial Data ---
# In a real application, this data would come from a database or a live API feed.
# Here, we are just storing it in memory.
mock_data = {
    "rbi_repo_rate": 6.50,
    "competitors": {
        "HDFC Bank": {"personal_loan_rate": 10.75, "processing_fee": 1.5},
        "ICICI Bank": {"personal_loan_rate": 11.25, "processing_fee": 1.25},
        "Bajaj Finserv": {"personal_loan_rate": 12.00, "processing_fee": 2.0},
    }
}


# --- 2. API Endpoint for RBI Repo Rate ---
@app.route('/api/v1/market/rbi-rate', methods=['GET'])
def get_rbi_rate():
    """
    Simulates an API endpoint to get the current RBI repo rate.
    The rate will fluctuate slightly to simulate market changes.
    """
    # Simulate a small, random fluctuation in the repo rate
    fluctuation = random.uniform(-0.05, 0.05)
    current_rate = mock_data["rbi_repo_rate"] + fluctuation

    response = {
        "rate": round(current_rate, 2),
        "last_updated": datetime.now().isoformat(),
        "source": "Reserve Bank of India (Simulated)"
    }
    return jsonify(response)


# --- 3. API Endpoint for Competitor Loan Offers ---
@app.route('/api/v1/market/competitor-offers', methods=['GET'])
def get_competitor_offers():
    """
    Simulates an API endpoint to get personal loan offers from competitors.
    """
    # We can also add slight fluctuations to competitor data
    updated_competitors = {}
    for bank, data in mock_data["competitors"].items():
        rate_fluctuation = random.uniform(-0.1, 0.1)
        updated_competitors[bank] = {
            "personal_loan_rate": round(data["personal_loan_rate"] + rate_fluctuation, 2),
            "processing_fee": data["processing_fee"]
        }

    response = {
        "offers": updated_competitors,
        "last_updated": datetime.now().isoformat(),
        "source": "Aggregated Market Data (Simulated)"
    }
    return jsonify(response)


# --- 4. Root Endpoint for Health Check ---
@app.route('/')
def index():
    """A simple root endpoint to confirm the server is running."""
    return "<h1>Mock Financial API Server is running!</h1>" + \
        "<p>Available endpoints:</p>" + \
        "<ul><li><a href='/api/v1/market/rbi-rate'>/api/v1/market/rbi-rate</a></li>" + \
        "<li><a href='/api/v1/market/competitor-offers'>/api/v1/market/competitor-offers</a></li></ul>"


# --- 5. Main Execution Block ---
if __name__ == '__main__':
    # This makes the script runnable directly from the command line.
    # It will start the web server on your local machine.
    # The default address is http://127.0.0.1:5000
    print("--- Starting Mock Financial API Server ---")
    print("Server is running at http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")
    app.run(debug=True, port=5000)
