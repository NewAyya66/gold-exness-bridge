from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

TWELVE_KEY = os.environ.get('TWELVE_DATA_KEY', '')
current_price = 2038.50

def fetch_realtime_price():
    global current_price
    if TWELVE_KEY:
        try:
            r = requests.get(f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={TWELVE_KEY}", timeout=5)
            data = r.json()
            if data.get('price'):
                current_price = float(data['price'])
                return current_price
        except:
            pass
    # Fallback simulation
    change = (random.random() - 0.5) * 1.8
    current_price = max(1920, min(2180, current_price + change))
    return current_price

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Exness Demo Bridge",
        "endpoints": ["/price", "/status", "/ping"]
    })

@app.route('/ping')
def ping():
    return jsonify({"pong": True, "timestamp": datetime.now().isoformat()})

@app.route('/status')
def status():
    return jsonify({
        "online": True,
        "service": "gold-bridge",
        "last_price": current_price,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/price')
def price():
    p = fetch_realtime_price()
    return jsonify({
        "symbol": "XAUUSD",
        "bid": p,
        "ask": round(p + 0.35, 2),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
