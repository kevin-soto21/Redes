#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import socket

# ====== CREDENCIALES EN TEXTO PLANO ======
USUARIOS = {
    "Lupe": "REDES",
    "Kevin": "REDES",
    "Carlos": "REDES"
}

SECRET_KEY = "REDES"

# ====== CONFIGURACIÓN TCP ======
TCP_HOST = "127.0.0.1"
TCP_PORT = 5001

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
app.secret_key = SECRET_KEY


def is_logged_in():
    return session.get("logged_in") is True


def send_cmd(cmd: str) -> str:
    try:
        # Timeout de 8 segundos para el movimiento suave
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=8) as s:
            s.sendall((cmd.strip() + "\n").encode("utf-8"))
            data = b""
            while b"\n" not in data:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            return data.decode("utf-8", errors="ignore").strip()
    except socket.timeout:
        return "ERROR: Tiempo de espera agotado"
    except Exception as e:
        return f"ERROR: {str(e)}"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "")

        # --- LÍNEA 51: VALIDACIÓN CORREGIDA ---
        if user in USUARIOS and USUARIOS[user] == pw:
            session["logged_in"] = True
            session["username"] = user
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

    angle = max(0, min(180, angle))

    cmd = ("S" if smooth5s else "A") + f" {angle}"
    resp = send_cmd(cmd)

    is_ok = resp.startswith("OK") or resp.startswith("CONFIRMACION")

    return jsonify({
        "ok": is_ok,
        "cmd": cmd,
        "resp": resp,
        "angle": angle,
        "user": session.get("username")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
