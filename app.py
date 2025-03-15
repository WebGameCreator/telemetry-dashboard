from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
import webbrowser
import requests
import os

app = Flask(__name__, static_url_path="/")
socketio = SocketIO(app)
wsgi_app = app.wsgi_app

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

saved_telemtry = []

def send_telemetry():
    while True:
        try:
            response = requests.get("https://api.v2.sondehub.org/amateur/telemetry?duration=7d&payload_callsign=PC9DB")
            data = response.json()
            data = data[list(data.keys())[0]]
            for key in data:
                if key in saved_telemtry:
                    continue
                saved_telemtry.append(key)
                payload = data[key]
                telemetry = {
                    "latitude": payload["lat"],
                    "longitude": payload["lon"],
                    "altitude": payload["alt"],
                    "temperature": payload["temp"],
                    "time": payload["time_received"]
                }
                socketio.emit("updateData", telemetry)
                break # break, so it doesn't send all data at once

        except Exception as e:
            print(f"Error fetching telemetry data: {e}")
        socketio.sleep(2)

thread = Thread(target=send_telemetry)
thread.start()

HOST = os.environ.get("SERVER_HOST", "localhost")
PORT = int(os.environ.get("SERVER_PORT", "5555"))

webbrowser.open("http://localhost:" + str(PORT), new=2)
socketio.run(app, host=HOST, port=PORT)
