from prometheus_client import start_http_server, generate_latest
from flask import Flask, Response
import threading

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

def run_dashboard(port=8000):
    start_http_server(port)
    app.run(port=port+1)

def start_monitoring():
    thread = threading.Thread(target=run_dashboard, daemon=True)
    thread.start()
