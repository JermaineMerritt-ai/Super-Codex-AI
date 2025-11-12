#!/usr/bin/env python3
"""Simple test Flask app to verify Flask works"""

from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return "Simple Test Flask App - Working!"

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.datetime.utcnow().isoformat()})

if __name__ == "__main__":
    print("Starting simple test Flask app...")
    app.run(host="127.0.0.1", port=8085, debug=False)
    print("Flask app finished.")