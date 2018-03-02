from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from jinja2 import Environment, FileSystemLoader
import os
import urllib
import datetime
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

j2_env = Environment(loader=FileSystemLoader(THIS_DIR + "/views"), trim_blocks=True)

class MyHandler(BaseHTTPRequestHandler):
    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(60)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

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

        rendered = j2_env.get_template("index.html").render(logs=logs, durations_json=json.dumps(durations))
        self.wfile.write(rendered)

    def do_HEAD(self):
        self._set_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 3001
    httpd = ThreadedHTTPServer((ip, port), MyHandler)
    print("Running server at %s:%d..." % (ip, port))
    httpd.serve_forever()
