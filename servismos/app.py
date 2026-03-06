#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash
import socket

# ====== CREDENCIALES ======
APP_USER = "Lupe"
APP_PW_HASH = "scrypt:32768:8:1$lyub1caXMpfcp1f6$cfe16e2c9b6b956787f32f9d035f37ed34c860faeb23f5d2366ce7b136a4b7ae25afb456aa6604861f2d5f99398a0afb64fbafd5678fb6461f120d96ae449ad1"
SECRET_KEY = "REDES"

# ====== TCP hacia servidor_tcp.py ======
TCP_HOST = "127.0.0.1"
TCP_PORT = 5001

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
app.secret_key = SECRET_KEY


def is_logged_in():
    return session.get("logged_in") is True


def send_cmd(cmd: str) -> str:
    with socket.create_connection((TCP_HOST, TCP_PORT), timeout=3) as s:
        s.sendall((cmd.strip() + "\n").encode("utf-8"))
        data = b""
        while b"\n" not in data:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        return data.decode("utf-8", errors="ignore").strip()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "")

        if user == APP_USER and check_password_hash(APP_PW_HASH, pw):
            session["logged_in"] = True
            return redirect(url_for("index"))

        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html", error=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("index.html")


@app.post("/api/servo")
@app.post("/set_servo")
def set_servo():
    if not is_logged_in():
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}
    angle = int(data.get("angle", 90))
    smooth5s = bool(data.get("smooth5s", True))

    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180

    # Arduino entiende:
    # A <angulo> -> directo
    # S <angulo> -> suave 5s (en el .ino)
    cmd = ("S" if smooth5s else "A") + f" {angle}"
    resp = send_cmd(cmd)

    return jsonify({
        "ok": resp.startswith("OK"),
        "cmd": cmd,
        "resp": resp,
        "angle": angle,
        "smooth5s": smooth5s
    })


@app.get("/api/ping")
def ping():
    if not is_logged_in():
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
