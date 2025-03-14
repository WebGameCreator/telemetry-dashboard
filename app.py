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
        try:
            # Fetch telemetry data from SondeHub API
            response = requests.get("https://api.v2.sondehub.org/payloads?user-agent=weather-balloon-project")
            data = response.json()
            
            if data:
                # Extracting relevant information from the first payload
                payload = data[0]
                telemetry = {
                    "latitude": payload.get("lat", None),
                    "longitude": payload.get("lon", None),
                    "altitude": payload.get("alt", None),
                    "temperature": payload.get("temp", None),  # If temperature is available
                    "time": payload.get("time_received", None)  # Time of last update
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
