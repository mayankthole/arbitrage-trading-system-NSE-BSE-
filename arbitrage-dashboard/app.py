from flask import Flask, render_template, jsonify
import requests
import json
import time
import threading
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Your Dhan API credentials
client_id = "1106534888"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ3NjQ2MDMzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjUzNDg4OCJ9.TrT8U_uS3TEqqF23VGBgc1_SHk9f3S0e6yp_tbRdZ97A_93bZuYNcUul9JvGxme4_8bd3rvgyUnuzdNa9Y8QYA"

# API endpoint
url = "https://api.dhan.co/v2/marketfeed/ltp"

# Headers required by Dhan API
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'access-token': access_token,
    'client-id': client_id
}

# Security IDs for NSE and BSE
data = {
    "NSE_EQ": [2277],  # Security ID for NSE
    "BSE_EQ": [500290]  # Security ID for BSE
}

# Global variables to store data
current_data = None
historical_data = []
best_opportunity = {
    "spread_percent": 0,
    "timestamp": None,
    "nse_price": 0,
    "bse_price": 0,
    "diff": 0
}
is_monitoring = False
monitor_thread = None

def fetch_prices_with_arbitrage():
    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        
        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Process the response
        if response.status_code == 200:
            result = response.json()
            
            # Extract NSE price
            nse_price = result["data"]["NSE_EQ"]["2277"]["last_price"]
            
            # Extract BSE price
            bse_price = result["data"]["BSE_EQ"]["500290"]["last_price"]
            
            # Calculate price difference and spread
            price_diff = abs(nse_price - bse_price)
            lower_price = min(nse_price, bse_price)
            percentage_spread = (price_diff / lower_price) * 100
            
            # Log information
            logger.info(f"NSE: ₹{nse_price:.2f}, BSE: ₹{bse_price:.2f}, Spread: {percentage_spread:.4f}%")
            
            # Return the data for processing
            return {
                "timestamp": current_time,
                "nse_price": nse_price,
                "bse_price": bse_price,
                "diff": price_diff,
                "spread_percent": percentage_spread,
                "arbitrage_opportunity": percentage_spread > 0.05
            }
            
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return None

def monitoring_task():
    global current_data, historical_data, best_opportunity, is_monitoring
    
    logger.info("Starting monitoring thread")
    
    while is_monitoring:
        result = fetch_prices_with_arbitrage()
        
        if result:
            # Update current data
            current_data = result
            
            # Add to historical data (keeping last 100 points)
            historical_data.append(result)
            if len(historical_data) > 100:
                historical_data = historical_data[-100:]
            
            # Update the best opportunity if applicable
            if result["spread_percent"] > best_opportunity["spread_percent"]:
                best_opportunity = {
                    "spread_percent": result["spread_percent"],
                    "timestamp": result["timestamp"],
                    "nse_price": result["nse_price"],
                    "bse_price": result["bse_price"],
                    "diff": result["diff"]
                }
                logger.info(f"New best opportunity: {best_opportunity['spread_percent']:.4f}%")
        
        time.sleep(1)  # Wait for 1 second before the next update
    
    logger.info("Monitoring thread stopped")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_monitoring', methods=['POST'])
def start_monitoring():
    global is_monitoring, monitor_thread
    
    if not is_monitoring:
        is_monitoring = True
        monitor_thread = threading.Thread(target=monitoring_task)
        monitor_thread.daemon = True
        monitor_thread.start()
        return jsonify({"status": "started"})
    
    return jsonify({"status": "already_running"})

@app.route('/api/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global is_monitoring
    
    if is_monitoring:
        is_monitoring = False
        return jsonify({"status": "stopped"})
    
    return jsonify({"status": "not_running"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        "current": current_data,
        "historical": historical_data,
        "best": best_opportunity
    })

if __name__ == '__main__':
    app.run(debug=True)