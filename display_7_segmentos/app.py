from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)

TCP_HOST = "127.0.0.1"
TCP_PORT = 5001

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_number", methods=["POST"])
def set_number():
    data = request.get_json()

    numero = str(data.get("number", ""))

    if numero not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return jsonify({
            "success": False,
            "message": "Número inválido"
        })

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((TCP_HOST, TCP_PORT))

        cliente.sendall(numero.encode())

        respuesta = cliente.recv(1024).decode()
        cliente.close()

        return jsonify({
            "success": True,
            "number": numero,
            "message": respuesta
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error al conectar con servidor TCP: {e}"
        })

if __name__ == "__main__":
    app.run(debug=True)
