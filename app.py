import os
from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

current_price = 2038.50

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Gold Price API is running!",
        "endpoints": ["/price", "/status"]
    })

@app.route('/price')
def get_price():
    global current_price
    change = (random.random() - 0.5) * 2.0
    current_price = max(1900, min(2200, current_price + change))
    return jsonify({
        "symbol": "XAUUSD",
        "bid": round(current_price, 2),
        "ask": round(current_price + 0.35, 2),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/status')
def get_status():
    return jsonify({
        "online": True,
        "last_price": round(current_price, 2)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
