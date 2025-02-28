from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
import os
import random
import webbrowser

app = Flask(__name__, static_url_path="/")
socketio = SocketIO(app)
wsgi_app = app.wsgi_app

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

def send_telemetry():
    while True:
        # Currently emits random numbers for testing
        # To do: Get real data from amateur.sondehub.org or tinygs.com
        socketio.emit("updateData", { "data": random.randint(0, 6) })
        socketio.sleep(2)

thread = Thread(target=send_telemetry)
thread.start()

HOST = os.environ.get("SERVER_HOST", "localhost")
PORT = int(os.environ.get("SERVER_PORT", "5555"))

webbrowser.open("http://localhost:" + str(PORT), new=2)
socketio.run(app, host=HOST, port=PORT)
