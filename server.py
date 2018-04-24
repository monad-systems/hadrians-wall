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

    return render_template("index.html", logs=logs, logs_json=json.dumps(logs))

with app.test_request_context():
    url_for('static', filename='style.css')
