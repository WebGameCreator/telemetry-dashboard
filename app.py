from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
import os
import random

app = Flask(__name__, static_url_path="/")
socketio = SocketIO(app)
wsgi_app = app.wsgi_app

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

def send_telemetry():
    while True:
        # Emits a random number for testing
        socketio.emit("updateData", { "data": random.randint(0, 9) })
        socketio.sleep(2)

thread = Thread(target=send_telemetry)
thread.start()

HOST = os.environ.get("SERVER_HOST", "localhost")
PORT = int(os.environ.get("SERVER_PORT", "5555"))
socketio.run(app, host=HOST, port=PORT)
