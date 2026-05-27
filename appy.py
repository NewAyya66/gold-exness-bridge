import os
from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

# Create the app
app = Flask(__name__)
CORS(app)

# Store the current price
current_price = 2038.50

@app.route('/')
def home():
    return 'Gold Price API is running! Use /price or /status'

@app.route('/price')
def price():
    global current_price
    # Simple price movement
    change = (random.random() - 0.5) * 2
    current_price = current_price + change
    if current_price < 1900:
        current_price = 1900
    if current_price > 2200:
        current_price = 2200
    
    return {
        'bid': round(current_price, 2),
        'ask': round(current_price + 0.35, 2),
        'symbol': 'XAUUSD',
        'timestamp': datetime.now().isoformat()
    }

@app.route('/status')
def status():
    return {'online': True, 'price': round(current_price, 2)}

# This is the key - it MUST be at the bottom
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
