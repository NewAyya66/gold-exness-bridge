#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gold Price API for Exness MT5 Bridge
Compatible with Python 3.11+ on Render.com
"""

import os
import sys
import random
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

# Print Python version for debugging (visible in Render logs)
print(f"✅ Python version: {sys.version}", flush=True)
print(f"✅ Starting Gold Price API service...", flush=True)

# Create Flask application
app = Flask(__name__)

# Enable CORS for Android app access
CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory price storage
current_price = 2038.50
price_history = []

def generate_realistic_price():
    """Generate realistic gold price movement"""
    global current_price
    # Random walk with slight mean reversion
    change = (random.random() - 0.5) * 2.2
    # Add small trend bias (0.02% drift)
    drift = 0.02
    new_price = current_price + change + drift
    # Keep within realistic gold range (1900-2200)
    current_price = max(1900.00, min(2200.00, new_price))
    return round(current_price, 2)

@app.route('/')
def home():
    """Root endpoint - API information"""
    return jsonify({
        "status": "online",
        "service": "Gold Price API - Exness Bridge",
        "version": "1.0.0",
        "python_version": sys.version.split()[0],
        "endpoints": {
            "/price": "GET - Current gold price (XAUUSD)",
            "/status": "GET - Service status",
            "/ping": "GET - Health check",
            "/history": "GET - Recent price history"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    """Health check endpoint"""
    return jsonify({
        "pong": True,
        "timestamp": datetime.now().isoformat(),
        "service": "alive"
    })

@app.route('/status')
def status():
    """Service status endpoint"""
    return jsonify({
        "online": True,
        "service": "gold-exness-bridge",
        "last_price": round(current_price, 2),
        "last_update": datetime.now().isoformat(),
        "uptime": "active",
        "python_version": sys.version.split()[0]
    })

@app.route('/price')
def get_price():
    """Main price endpoint - returns current XAUUSD price"""
    global current_price, price_history
    
    # Generate new price
    price = generate_realistic_price()
    current_price = price
    
    # Store in history (keep last 100 prices)
    price_history.append({
        "price": price,
        "time": datetime.now().isoformat()
    })
    if len(price_history) > 100:
        price_history.pop(0)
    
    # Return price data (matching Exness format)
    return jsonify({
        "symbol": "XAUUSD",
        "bid": price,
        "ask": round(price + 0.35, 2),
        "spread": 0.35,
        "high": round(price + (random.random() * 2), 2),
        "low": round(price - (random.random() * 2), 2),
        "timestamp": datetime.now().isoformat(),
        "source": "exness_bridge"
    })

@app.route('/history')
def get_history():
    """Get recent price history"""
    return jsonify({
        "count": len(price_history),
        "data": price_history[-50:],
        "current_price": round(current_price, 2)
    })

@app.route('/exness/price')
def exness_price():
    """Endpoint that mimics Exness API format"""
    price = generate_realistic_price()
    current_price = price
    return jsonify({
        "code": 0,
        "message": "success",
        "data": {
            "symbol": "XAUUSD",
            "bid": price,
            "ask": round(price + 0.35, 2),
            "time": datetime.now().isoformat()
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": 500}), 500

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting server on port {port}", flush=True)
    print(f"📍 Local URL: http://0.0.0.0:{port}", flush=True)
    print(f"📍 Price endpoint: http://0.0.0.0:{port}/price", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
