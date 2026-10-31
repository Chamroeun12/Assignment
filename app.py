import os
import socket
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Retrieve application version from environment variable with fallback default
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")


@app.route("/")
def index():
    hostname = socket.gethostname()
    return render_template(
        "index.html",
        title="CI/CD Homework 2",
        version=APP_VERSION,
        hostname=hostname
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "hostname": socket.gethostname()
    }), 200


@app.route("/api/info")
def api_info():
    return jsonify({
        "service": "cicd-assignment-backend",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "runtime": "python-flask",
        "cluster": "docker-swarm"
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
