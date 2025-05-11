import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import yaml
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

TARGETS_CACHE = {
    "data": [],
    "last_loaded": 0,
    "reload_interval": 5  # seconds
}

def load_targets():
    with open("targets.yaml") as f:
        return yaml.safe_load(f)

def get_targets():
    now = time.time()
    if now - TARGETS_CACHE["last_loaded"] > TARGETS_CACHE["reload_interval"]:
        print(">>> Reloading targets.yaml")
        TARGETS_CACHE["data"] = load_targets()
        TARGETS_CACHE["last_loaded"] = now
    return TARGETS_CACHE["data"]

def ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", host])
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Ping error for {host}: {e}")
        return False

def get_ping_results():
    targets = get_targets()
    return [
        {
            "label": target["label"],
            "status": "up" if ping(target["host"]) else "down"
        }
        for target in targets
    ]

@app.route("/")
def index():
    return render_template("index.html")

def background_ping_loop():
    print(">>> Background ping loop started")
    while True:
        results = get_ping_results()
        print(">>> Emitting results via WebSocket:", results)
        socketio.emit('ping_update', results, namespace='/')  # <- final fix
        time.sleep(2)

if __name__ == "__main__":
    socketio.start_background_task(background_ping_loop)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=True)
