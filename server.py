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

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


with app.test_request_context():
    url_for('static', filename='style.css')
