FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install flask flask-socketio eventlet pyyaml

EXPOSE 5000

CMD ["python", "app.py"]
