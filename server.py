from flask import Flask, url_for
from flask import render_template
import os
import urllib
import datetime
import json

app = Flask(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    files = os.listdir("hadrians-brick/logs")
    logs = []
    durations = []

    for file in files:
        entries = open('hadrians-brick/logs/' + file, 'r').read().split('\n')
        for entry in entries:
            try:
                log = json.loads(entry)
            except json.decoder.JSONDecodeError:
                continue
            logs.append(log)
            if log["exit-code"] == 0 and "mode" in log and log["mode"] == "default":
                durations.append({
                    "timestamp": log['timestamp'], 
                    "duration": float(log['duration']) / 60.0
                })

    return render_template("index.html", logs=logs, durations_json=json.dumps(durations))

with app.test_request_context():
    url_for('static', filename='style.css')
