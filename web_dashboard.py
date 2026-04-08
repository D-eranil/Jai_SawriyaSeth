"""Simple web dashboard server for ui/index.html driven by headless status.json."""
import json
import os
from flask import Flask, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")
IMG_DIR = os.path.join(BASE_DIR, "images")
STATUS_FILE = os.path.join(BASE_DIR, "data", "logs", "status.json")

app = Flask(__name__, static_folder=UI_DIR)


@app.route("/")
def index():
    return send_from_directory(UI_DIR, "index.html")


@app.route("/images/<path:name>")
def images(name):
    return send_from_directory(IMG_DIR, name)


@app.route("/api/status")
def status():
    if not os.path.exists(STATUS_FILE):
        return jsonify(
            {
                "capital": 0,
                "today_pnl": 0,
                "total_pnl": 0,
                "live_rates": {},
                "rates_history": {},
                "tg_last_messages": {},
                "mode": "OFFLINE",
            }
        )
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"error": "failed_to_read_status"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
