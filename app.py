import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import yaml
import time
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

def ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", host])
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Ping error for {host}: {e}")
        return False

def tcp_check(host, port, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception as e:
        print(f"TCP error for {host}:{port} -> {e}")
        return False

def check_target(target):
    method = target.get("check", "ping")
    host = target["host"]
    label = target["label"]

    if method == "ping":
        result = ping(host)
    elif method == "tcp":
        port = int(target.get("port", 80))
        result = tcp_check(host, port)
    else:
        print(f"Unknown check type for {label}: {method}")
        result = False

    return {"label": label, "status": "up" if result else "down"}

def get_ping_results():
    print(">>> Reloading targets.yaml")
    try:
        fd = os.open("targets.yaml", os.O_RDONLY)
        with os.fdopen(fd) as f:
            targets = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading targets.yaml: {e}")
        return []

    result_map = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_label = {executor.submit(check_target, t): t["label"] for t in targets}
        for future in as_completed(future_to_label, timeout=5):
            label = future_to_label[future]
            try:
                result = future.result(timeout=1.5)
            except Exception as e:
                print(f"Timeout/error checking {label}: {e}")
                result = {"label": label, "status": "down"}
            result_map[label] = result

    # Return results in original order
    return [result_map.get(t["label"], {"label": t["label"], "status": "down"}) for t in targets]

@app.route("/")
def index():
    return render_template("index.html")

def background_ping_loop():
    print(">>> Background ping loop started")
    while True:
        results = get_ping_results()
        print(">>> Emitting results via WebSocket:", results)
        socketio.emit('ping_update', results, namespace='/')
        time.sleep(2)

if __name__ == "__main__":
    socketio.start_background_task(background_ping_loop)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=True)
