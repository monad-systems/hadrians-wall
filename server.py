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
    contribs = {}

    for file in files:
        user = file.split('.')[0]
        entries = open('hadrians-brick/logs/' + file, 'r').read().split('\n')
        contribs[user] = len(entries)
        for entry in entries:
            try:
                log = json.loads(entry)
            except json.decoder.JSONDecodeError:
                continue
            logs.append(log)
    contribs = sorted(contribs.items(), key=lambda x:x[1])
    return render_template("index.html", logs=logs, logs_json=json.dumps(logs),
                           contribs=contribs)

with app.test_request_context():
    url_for('static', filename='style.css')
