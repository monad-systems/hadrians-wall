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
    files = os.listdir(THIS_DIR + "/static/logs")
    logs = []
    durations = []

    for file in files:
        if ".err" in file:
            prefix = file[0:-8]
            segments = prefix.split("%");
            log = {
                "datetime": datetime.datetime.strptime(segments[0], "%Y-%m-%dT%H:%M:%S.%f"),
                "mode": segments[1],
                "duration": float(segments[2]) / 60.0,
                "result": segments[3],
                "prefix": urllib.quote_plus(prefix)
            }
            logs.append(log)
            if log["result"] == "success" and log["mode"] =="default":
                durations.append({
                    "datetime": segments[0],
                    "duration": float(segments[2]) / 60.0
                })

    return render_template("index.html", logs=logs, durations_json=json.dumps(durations))

with app.test_request_context():
    url_for('static', filename='style.css')
