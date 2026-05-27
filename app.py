import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get API key from environment variable
API_KEY = os.environ.get('TWELVE_DATA_API_KEY', '')
current_price = 4436.00  # Starting near current gold price

def get_live_gold_price():
    """Fetch real gold price from Twelve Data"""
    global current_price
    
    if not API_KEY:
        print("WARNING: No API key found!")
        return current_price
    
    try:
        url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('price'):
            current_price = float(data['price'])
            return current_price
        else:
            print(f"API returned: {data}")
            return current_price
    except Exception as e:
        print(f"API Error: {e}")
        return current_price

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Live Gold Prices - Exness Compatible",
        "api_key_configured": bool(API_KEY),
        "current_price": round(current_price, 2),
        "message": "Use /price for live data"
    })

@app.route('/price')
def get_price():
    price = get_live_gold_price()
    return jsonify({
        "symbol": "XAUUSD",
        "bid": round(price, 2),
        "ask": round(price + 0.35, 2),
        "spread": 0.35,
        "timestamp": datetime.now().isoformat(),
        "source": "twelve_data_live" if API_KEY else "no_api_key"
    })

@app.route('/status')
def get_status():
    return jsonify({
        "online": True,
        "last_price": round(current_price, 2),
        "api_key_working": bool(API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
