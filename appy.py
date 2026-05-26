import sys
print("Python version:", sys.version)

from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app)

# Simple in-memory price
current_price = 2038.50

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Gold Price API",
        "message": "Working! Try /price or /status"
    })

@app.route('/ping')
def ping():
    return jsonify({"pong": True, "time": datetime.now().isoformat()})

@app.route('/status')
def status():
    return jsonify({
        "online": True,
        "service": "gold-bridge",
        "last_price": current_price,
        "python_version": sys.version[:5]
    })

@app.route('/price')
def price():
    global current_price
    # Simulate realistic price movement
    change = (random.random() - 0.5) * 2.0
    current_price = max(1900, min(2200, current_price + change))
    return jsonify({
        "symbol": "XAUUSD",
        "bid": round(current_price, 2),
        "ask": round(current_price + 0.35, 2),
        "spread": 0.35,
        "timestamp": datetime.now().isoformat(),
        "source": "exness_simulated"
    })

# This is CRITICAL - for Gunicorn to find the app
if __name__ != '__main__':
    # When running on Gunicorn (Render), this block runs
    pass

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
