from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
import os
import requests
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
        try:
            # Fetch telemetry data from SondeHub API
            response = requests.get("https://api.v2.sondehub.org/amateur/telemetry?duration=12h&payload_callsign=AG6NS-11")
            data = response.json()
            
            if data:
                # Extracting relevant information from the first payload
                payload = data["AG6NS-11"]["2025-03-14T06:30:29.000Z"]
                telemetry = {
                    "latitude": payload["lat"],
                    "longitude": payload["lon"],
                    "altitude": payload["alt"],
                    "temperature": payload["temp"],  # If temperature is available
                    "time": payload["time_received"] # Time of last update
                }

                # Emit the telemetry data via WebSocket
                socketio.emit("updateData", telemetry)
        
        except Exception as e:
            print(f"Error fetching telemetry data: {e}")
        socketio.sleep(2)

thread = Thread(target=send_telemetry)
thread.start()

HOST = os.environ.get("SERVER_HOST", "localhost")
PORT = int(os.environ.get("SERVER_PORT", "5555"))

webbrowser.open("http://localhost:" + str(PORT), new=2)
socketio.run(app, host=HOST, port=PORT)
